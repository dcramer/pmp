from .base import Command, registry, arg


@registry.add
class RegisterCommand(Command):
    """
    Registers the current project with a remote PyPi
    repository.
    """

    name = 'register'
    short_desc = 'Register a package'
    arguments = (
        arg('--check'),
    )

    def run(self, args, **options):
        print "Args:", args
        print "Kwargs:", options
