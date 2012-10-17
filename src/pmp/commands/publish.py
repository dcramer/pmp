from .base import Command, registry, arg


@registry.add
class PublishCommand(Command):
    """
    Publishes the current project to a remote PyPi repository.

    If the package has not yet been registered, you will be
    prompted to register first.

    The optional repository argument must already be configured,
    otherwise the default (e.g. pypi.python.org) will be used.
    """

    name = 'publish'
    short_desc = 'Publish a package'
    arguments = (
        arg('repository', help='remote repository name'),
    )

    def run(self, args, **options):
        print "Args:", args
        print "Kwargs:", options
