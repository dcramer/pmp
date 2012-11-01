from .base import Command, registry


@registry.add
class DevelopCommand(Command):
    """
    Installs development packages into the current environment and
    creates a symlink for your project (vs doing a hard copy as the
    normal install would)
    """

    name = 'develop'
    short_desc = 'Installs development packages'
    arguments = (
    )

    def main(self, args, **options):
        # pip install -e .
        pass
