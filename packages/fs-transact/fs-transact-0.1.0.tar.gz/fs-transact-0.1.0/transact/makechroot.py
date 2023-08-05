import argparse
import glob
import os
import shlex
import subprocess

"""
At this point we're inside the first `unshared` call. This create process/mount namespaces but doesn't abstract
the rootfs as we need to set up the rootfs first here with mounts inside the outer namespace.
"""


def make_overlay(lowerdir, upperdir, workdir, mountpoint, as_root=False):
    os.makedirs(mountpoint)
    os.makedirs(upperdir)
    os.makedirs(workdir)
    opts = f'lowerdir={shlex.quote(lowerdir)},upperdir={shlex.quote(upperdir)},workdir={shlex.quote(workdir)}'
    if not as_root:
        # When using an unprivileged userns this makes overlayfs not require root to delete directories
        opts += ',userxattr'
    cmd = ['mount', '-t', 'overlay', 'overlay', '-o', opts, mountpoint]
    res = subprocess.run(cmd)
    return res.returncode == 0


def fstype(mountpoint):
    res = subprocess.run(['findmnt', '-n', '-o', 'FSTYPE', mountpoint], capture_output=True)
    if res.returncode != 0:
        return None

    return res.stdout.decode().strip()


def prepare_env():
    shell = os.environ.get('SHELL', '/bin/sh')
    shellname = os.path.basename(shell)

    if shellname == "zsh":
        return {
            'ZDOTDIR': '/tmp/zshprompt',
        }

    return {}


def prepare_shell(rootfs):
    shell = os.environ.get('SHELL', '/bin/sh')
    shellname = os.path.basename(shell)

    if shellname == "zsh":
        zdotdir = os.environ.get('ZDOTDIR', os.path.expanduser('~'))
        rc = f'ZDOTDIR="{zdotdir}"\n'
        if os.path.isfile(os.path.join(zdotdir, '.zshenv')):
            rc += f'. "{os.path.join(zdotdir, ".zshenv")}"\n'
        if os.path.isfile(os.path.join(zdotdir, '.zshrc')):
            rc += f'. "{os.path.join(zdotdir, ".zshrc")}"\n'
        rc += 'PS1="(transact) $PS1"\n'
        os.makedirs(os.path.join(rootfs, 'tmp/zshprompt'))
        with open(os.path.join(rootfs, 'tmp/zshprompt/.zshrc'), 'w') as handle:
            handle.write(rc)
        os.chmod(os.path.join(rootfs, 'tmp/zshprompt/.zshrc'), 0o755)
        return [shell]
    else:
        return [shell]


def main():
    # Recreate paths from parent call
    parser = argparse.ArgumentParser()
    parser.add_argument('workdir')
    parser.add_argument('--asroot', action='store_true')
    args = parser.parse_args()
    workdir = args.workdir
    upper = os.path.join(workdir, 'upper')
    tempdir = os.path.join(workdir, 'tempdir')
    chroot = os.path.join(workdir, 'chroot')

    # Create chroot from the current rootfs with overlayfs mounts
    for path in glob.glob('/*'):
        if not os.path.isdir(path):
            continue

        mount_type = fstype(path)
        if mount_type in ['devtmpfs', 'proc', 'sysfs', 'tmpfs', 'vfat']:
            continue

        res = make_overlay(lowerdir=path,
                           upperdir=os.path.join(upper, path.lstrip('/')),
                           workdir=os.path.join(tempdir, path.lstrip('/')),
                           mountpoint=os.path.join(chroot, path.lstrip('/')),
                           as_root=args.asroot
                           )

        if not res:
            print(f"Failed to overlay mount {path}")

    # Add the system mounts
    os.makedirs(os.path.join(chroot, 'dev'))
    os.makedirs(os.path.join(chroot, 'proc'))
    os.makedirs(os.path.join(chroot, 'sys'))
    os.makedirs(os.path.join(chroot, 'tmp'))
    subprocess.run(['mount', '--rbind', '/dev', os.path.join(chroot, 'dev')])
    subprocess.run(['mount', '-t', 'proc', 'none', os.path.join(chroot, 'proc')])
    subprocess.run(['mount', '--rbind', '/sys', os.path.join(chroot, 'sys')])
    subprocess.run(['mount', '-t', 'tmpfs', 'tmpfs', os.path.join(chroot, 'tmp')])

    # Create a second namespace to abstract the filesystem to the overlayfs and run a shell
    new_env = os.environ.copy()
    new_env.update(prepare_env())
    subprocess.run(
        ['unshare', '--root', chroot, '--wd', os.getcwd()] + prepare_shell(chroot), env=new_env)


if __name__ == '__main__':
    main()
