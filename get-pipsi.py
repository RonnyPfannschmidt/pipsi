#!/usr/bin/env python
import os
import sys
from subprocess import call


def echo(msg=''):
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


def fail(msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()
    sys.exit(1)


def succeed(msg):
    echo(msg)
    sys.exit(0)


def command_exists(cmd):
    with open(os.devnull, 'w') as null:
        return call([cmd, '--version'], stdout=null, stderr=null) == 0


def main():
    print('Installing pipsi')
    bin_dir = os.path.expanduser('~/.local/bin')

    if os.name != 'posix':
        fail('So sorry, but pipsi only works on POSIX systems :(')

    if command_exists('pipsi'):
        succeed('You already have pipsi installed')

    if not command_exists('virtualenv'):
        fail('You need to have virtualenv installed to bootstrap pipsi.')

    try:
        os.makedirs(bin_dir)
    except OSError:
        pass

    import shutil
    venv = os.path.expanduser('~/.local/venvs/pipsi')

    def _cleanup():
        try:
            shutil.rmtree(venv)
        except (OSError, IOError):
            pass

    if call(['virtualenv', venv]) != 0:
        _cleanup()
        fail('Could not create virtualenv for pipsi :(')

    if call([venv + '/bin/pip', 'install', 'pipsi']) != 0:
        _cleanup()
        fail('Could not install pipsi :(')

    os.symlink(venv + '/bin/pipsi', bin_dir + '/pipsi')

    if not command_exists('pipsi') != 0:
        echo()
        echo('=' * 60)
        echo()
        echo('Warning:')
        echo('  It looks like ~/.local/bin is not on your PATH so pipsi will')
        echo('  not work out of the box.  To fix this problem make sure to')
        echo('  add this to your .bashrc / .profile file:')
        echo()
        echo('  export PATH=~/.local/bin:$PATH')
        echo()
        echo('=' * 60)
        echo()

    succeed('pipsi is now installed.')


if __name__ == '__main__':
    main()
