# Transact

This utility uses the userns feature of the kernel in combination with overlayfs to
run commands in a temporary container with your current filesystem as the starting
contents. After running the commands in this container you get the choice to apply
or throw away the changes made.

## Example

An example session showing the contents of the starting directory. Removing the codebase stored in this directory
and adding a new file. After exiting the shell spawned by `transact` the changes are shown and in this example
ignored.

```shell-session
~/P/P/transact ❯❯❯ ls
transact  transact.egg-info  README.md  setup.py
~/P/P/transact ❯❯❯ transact
(transact) ~/P/P/transact # ❯❯❯ ls
transact  transact.egg-info  README.md  setup.py
(transact) ~/P/P/transact # ❯❯❯ rm -rf transact
(transact) ~/P/P/transact # ❯❯❯ touch example
(transact) ~/P/P/transact # ❯❯❯ ls
transact.egg-info  README.md  example  setup.py
(transact) ~/P/P/transact # ❯❯❯ exit
M /home/martijn/.zhistory
D /home/martijn/Projects/Python/transact/transact
A /home/martijn/Projects/Python/transact/example
Do you want to commit these changes? [y/N] n
~/P/P/transact ❯❯❯ ls
transact  transact.egg-info  README.md  setup.py
```

## Acknowledgements

This project is inspired by https://github.com/binpash/try

The major differences are that this is written in Python and this allocates a PTY for the shell.
This also launches a shell instead of running only one command.