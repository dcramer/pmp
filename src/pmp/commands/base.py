__all__ = ('CommandRegistry', 'Command', 'Argument')


from pmp.cli import Argument  # NOQA


class CommandRegistry(dict):
    def add(self, cls):
        assert cls.name, 'missing name attribute on %r' % (cls,)
        assert cls.short_desc, 'missing short_desc attribute on %r' % (cls,)

        self[cls.name] = cls

        return cls


class Command(object):
    name = ''
    short_desc = ''
    arguments = ()

    def get_arguments(self):
        return [a for a in self.arguments if a.positional]

    def get_options(self):
        return [a for a in self.arguments if not a.positional]

    def run(self, **options):
        raise NotImplementedError

arg = Argument
registry = CommandRegistry()
