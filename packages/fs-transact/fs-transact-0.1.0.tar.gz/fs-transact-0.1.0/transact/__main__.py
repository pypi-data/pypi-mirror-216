import argparse
import fcntl
import os
import pty
import select
import shutil
import signal
import stat
import sys
import tempfile

import termios
import tty

from transact.util import prompt_bool

try:
    import colorama

    color_support = True
except ImportError:
    color_support = False

from transact.loopback import get_loopback_call


def print_red(*args):
    if not color_support:
        return print(*args)
    data = ' '.join(map(str, args))
    print(colorama.Fore.RED + data + colorama.Style.RESET_ALL)


def print_yellow(*args):
    if not color_support:
        return print(*args)
    data = ' '.join(map(str, args))
    print(colorama.Fore.YELLOW + data + colorama.Style.RESET_ALL)


def print_green(*args):
    if not color_support:
        return print(*args)
    data = ' '.join(map(str, args))
    print(colorama.Fore.GREEN + data + colorama.Style.RESET_ALL)


def subprocess_pty(args):
    # Simulate a pty-backed subprocess.run
    argv = list(args)
    pid, pty_fd = pty.fork()
    if pid == pty.CHILD:
        os.execvp(argv[0], argv)

    # FD of the tty running transact
    term_fd = sys.stdin.fileno()
    old = termios.tcgetattr(term_fd)

    def restore(*args):
        termios.tcsetattr(term_fd, termios.TCSAFLUSH, old)
        signal.signal(signal.SIGWINCH, old_sigwinch)

    def window_size_changed(*args):
        size = bytearray(4)
        fcntl.ioctl(term_fd, termios.TIOCGWINSZ, size)
        fcntl.ioctl(pty_fd, termios.TIOCSWINSZ, size)

    signal.signal(signal.SIGINT, restore)
    tty.setraw(pty.STDIN_FILENO)
    window_size_changed()

    # Transfer over window size changes
    old_sigwinch = signal.signal(signal.SIGWINCH, window_size_changed)

    # Copy data between the terminals
    while True:
        rfds, wfds, xfds = select.select([pty_fd, term_fd], [], [])

        if pty_fd in rfds:
            try:
                data = os.read(pty_fd, 1024)
            except OSError:
                break
            if not data:
                break
            os.write(sys.stdout.fileno(), data)

        if term_fd in rfds:
            try:
                data = os.read(term_fd, 1024)
            except OSError:
                break
            if not data:
                break
            while data != b'':
                written = os.write(pty_fd, data)
                data = data[written:]

    # PTY or stdin is closed, clean up
    restore()


def make_namespace(scratch_location):
    sandbox = tempfile.TemporaryDirectory(prefix="transact-", dir=scratch_location)
    workdir = sandbox.name

    upper = os.path.join(workdir, 'upper')
    tempdir = os.path.join(workdir, 'tempdir')
    chroot = os.path.join(workdir, 'chroot')
    os.makedirs(upper)
    os.makedirs(tempdir)
    os.makedirs(chroot)
    extra = []
    if os.geteuid() == 0:
        extra = ['--asroot']
    subprocess_pty(
        ['unshare', '--mount', '--map-root-user', '--user', '--pid', '--fork'] + get_loopback_call(
            'makechroot') + extra + [
            workdir])

    show_changes(upper)
    if prompt_bool("Do you want to commit these changes?"):
        apply_upper(upper)

    sandbox.cleanup()


def show_changes(upper):
    for root, dirs, files in os.walk(upper, topdown=True):
        for d in dirs:
            upper_dir = os.path.join(root, d)
            lower_dir = upper_dir[len(upper):]
            if not os.path.isdir(lower_dir):
                # This is a new directory, don't display all the contents in the diff
                dirs.remove(d)
                print_green("A " + lower_dir + "/")

        for f in files:
            upper_file = os.path.join(root, f)
            lower_file = upper_file[len(upper):]
            f_stat = os.stat(upper_file)
            if stat.S_ISCHR(f_stat.st_mode):
                print_red('D ' + lower_file)
            elif os.path.isfile(lower_file):
                print_yellow('M ' + lower_file)
            else:
                print_green('A ' + lower_file)


def apply_upper(upper):
    for root, dirs, files in os.walk(upper, topdown=True):
        for d in dirs:
            upper_dir = os.path.join(root, d)
            lower_dir = upper_dir[len(upper):]
            d_stat = os.stat(upper_dir)

            if not os.path.isdir(lower_dir):
                os.mkdir(lower_dir, d_stat.st_mode)

        for f in files:
            upper_file = os.path.join(root, f)
            lower_file = upper_file[len(upper):]
            f_stat = os.stat(upper_file)
            if stat.S_ISCHR(f_stat.st_mode):
                # Whiteout might be a file or a directory tree
                if os.path.isdir(lower_file):
                    shutil.rmtree(lower_file)
                else:
                    os.unlink(lower_file)
            else:
                shutil.copy2(upper_file, lower_file, follow_symlinks=False)


def main():
    parser = argparse.ArgumentParser(description="Filesystem transaction layer")
    parser.add_argument('--workdir', help='Override the location for the temporary rootfs and mountpoints')
    args = parser.parse_args()
    if color_support:
        colorama.init()

    scratch_dir = os.path.join(os.path.expanduser(os.environ.get('XDG_CACHE_HOME', '~/.cache')), 'transact')
    if args.workdir is not None:
        if not os.path.isdir(args.workdir):
            print("Selected work dir does not exist")
            exit(1)
        scratch_dir = os.path.abspath(os.path.expanduser(args.workdir))
    else:
        os.makedirs(scratch_dir, exist_ok=True)
    make_namespace(scratch_dir)


if __name__ == '__main__':
    main()
