from __future__ import absolute_import

from .base import Command, registry, arg
from pmp.shell import sh, colors


@registry.add
class InstallCommand(Command):
    """
    Installs packages the current environment.

    Package name can be any of the following recognized formats:

    - pkg-name
    - pkg-name==1.0.0
    - pkg-name==1.0.*

    GitHub and BitBucket shortcuts are also supported:

    - github.com/user/pkg-name
    - bitbucket.com/user/pkg-name

    If you do not pass an argument, '.' is assumed, which is equivilent
    to running this command without arguments.
    """

    name = 'install'
    short_desc = 'Install a package'
    arguments = (
        arg('package', help='package name to install', required=False,
            multiple=True),
        # arg('--dry-run'),
    )

    def main(self, packages):
        if not packages:
            packages = ['.']
        # TODO: this command should reach into the pip internals to pull out the available arguments,
        # as well as for installing the packages (so we're not piping stdout/etc).
        self.stream.write('Installing packages %s%s' % (colors.OKBLUE, ', '.join(map(repr, packages))))
        sh('pip', 'install', '--use-mirrors', *packages)
        self.stream.write('Successfully installed %s packages' % len(packages))
