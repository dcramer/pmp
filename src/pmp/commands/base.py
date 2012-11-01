from __future__ import absolute_import

__all__ = ('CommandRegistry', 'Command', 'Argument')


from pmp.argparser import Argument  # NOQA


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

    def __init__(self, stream, **kwargs):
        self.stream = stream

    def get_arguments(self):
        return [a for a in self.arguments if a.positional]

    def get_options(self):
        return [a for a in self.arguments if not a.positional]

    def get_usage(self):
        output = []
        for option in self.get_options():
            if not option.required:
                continue
            output.append(option.name)

        for arg in self.get_arguments():
            if not arg.required:
                if arg.multiple:
                    output.append('[{0}1] ... [{0}N]'.format(arg.name))
                else:
                    output.append('[{0}]'.format(arg.name))
            else:
                if arg.multiple:
                    output.append('{0}1 ... [{0}N]'.format(arg.name))
                else:
                    output.append(arg.name)

        return ' '.join(output)

    def main(self, **options):
        raise NotImplementedError

arg = Argument
registry = CommandRegistry()
