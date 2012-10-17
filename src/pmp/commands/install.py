from .base import Command, registry, arg


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
        arg('package', help='package name to install', required=True, multiple=True),
        arg('--dry-run'),
    )

    def run(self, args, **options):
        print "Args:", args
        print "Kwargs:", options
