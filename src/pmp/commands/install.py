from .base import Command, registry, arg


@registry.add
class InstallCommand(Command):
    """
    Installs a package into the current environment.

    Package name can be any of the following recognized formats:

    - pkg-name
    - pkg-name==1.0.0
    - pkg-name==1.0.*

    GitHub and BitBucket shortcuts are also supported:

    - github.com/user/pkg-name
    - bitbucket.com/user/pkg-name
    """

    name = 'install'
    short_desc = 'Installs a package'
    arguments = (
        arg('package', help='package name to install'),
        arg('--dry-run'),
    )

    def run(self, args, **options):
        print "Args:", args
        print "Kwargs:", options
