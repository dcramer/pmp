from __future__ import absolute_import

import inspect
import sys
from .shell import colors


def color_output(message, color=None):
    if color:
        output = color
    else:
        output = ""
    output += message
    output += colors.ENDC
    return output


class ArgumentError(Exception):
    pass


class Argument(object):
    def __init__(self, name, var=None, help='', required=False, multiple=False):
        self.name = name
        self.var = var  # same as dest in optparse
        self.help = help
        self.required = required
        self.multiple = multiple

    def __eq__(self, other):
        if isinstance(other, Argument):
            return self == other
        return self.name == other

    @property
    def positional(self):
        return not self.name.startswith('-')


class Formatter(object):
    def __init__(self, parser, colors=colors):
        self.parser = parser
        self.colors = colors
        self.name = 'pmp'

    def write(self, message, color=None):
        print color_output(message, color)

    def print_basic_usage(self, usage="[options] command [arguments]"):
        self.write("Usage:", colors.WARNING)
        self.write("  %s %s" % (self.name, usage))
        self.write("")

    def print_full_usage(self):
        self.print_basic_usage()

        self.write("Available commands:", colors.WARNING)
        max_cmd_len = max(max(len(c.name) for c in self.parser.get_subcommands()), 10)
        template = "  %s{0:%s}%s   {1}" % (colors.OKGREEN, max_cmd_len, colors.ENDC)

        for command in self.parser.get_subcommands():
            self.write(template.format(command.name, command.short_desc))

    def print_command_usage(self, command):
        self.print_basic_usage('%s %s' % (command.name, command.get_usage()))

        arguments = command.get_arguments()
        if arguments:
            max_cmd_len = max(max(len(a.name) for a in arguments), 10)
            template = "  %s{0:%s}%s   {1}" % (colors.OKGREEN, max_cmd_len, colors.ENDC)
            self.write('Arguments:', colors.WARNING)
            for arg in arguments:
                self.write(template.format(arg.name, arg.help))
            self.write("")

        options = command.get_options()
        if options:
            max_cmd_len = max(max(len(a.name) for a in options), 10)
            template = "  %s{0:%s}%s   {1}" % (colors.OKGREEN, max_cmd_len, colors.ENDC)
            self.write('Options:', colors.WARNING)
            for opt in options:
                self.write(template.format(opt.name, opt.help))
            self.write("")

        docstring = inspect.getdoc(command)
        if docstring:
            self.write('Help:', colors.WARNING)
            self.write('  %s' % (docstring.replace('\n', '\n  '),))


class CommandParser(object):
    """
    Simple extension to OptionParser which handles a single subcommand.
    """
    def __init__(self, subcommands, formatter=Formatter, **kwargs):
        self.subcommands = subcommands
        self.stream = formatter(self)

    def parse_args(self, argv):
        main_args, cmd_name, cmd_args = self.parse_subcommand(argv)

        # this might be a full fledged command
        if cmd_name is None:
            self.main(cmd_args)

        elif cmd_name == 'help':
            if cmd_args:
                self.print_help(cmd_args, cmd_args[1:])
            else:
                self.print_help(None, cmd_args)
            sys.exit(1)

        # Parser main options
        # TODO:
        # (main_options, _) = self.parser.parse_args(main_args)

        if cmd_name not in self.subcommands:
            self.stream.print_basic_usage()
            self.stream.write("\nERROR: No command by the name %r" % (cmd_name,), colors.FAIL)
            sys.exit(1)

        command = self.subcommands[cmd_name](self.stream)

        try:
            cmd_args, cmd_options = self.parse_command_args(command, cmd_args)
        except ArgumentError, exc:
            self.print_help(cmd_name, cmd_args)
            self.stream.write("\nERROR: %r is not valid argument" % (str(exc),), colors.FAIL)
            sys.exit(1)

        return command, cmd_args, cmd_options

    def parse_command_args(self, command, cmd_args):
        all_args = command.arguments

        args, kwargs = [], {}
        for arg in cmd_args:
            if arg.startswith('-'):
                if arg.startswith('--'):
                    if '=' in arg:
                        arg, argvalue = arg.split('=', 1)
                    else:
                        arg, argvalue = arg, True
                    argname = arg[2:]
                else:
                    argvalue = True
                    argname = arg[1:]

                argname = argname.replace('-', '_')

                # TODO: make this faster
                if arg not in all_args:
                    raise ArgumentError(arg)
                kwargs[argname] = argvalue
            else:
                args.append(arg)
        return args, kwargs

    def parse_subcommand(self, args):
        """
        This parses the arguments and returns a tuple containing:

        (args, command, command_args)

        For example, "--config=bar start --with=baz" would return:

        (['--config=bar'], 'start', ['--with=baz'])
        """
        index = None
        for arg_i, arg in enumerate(args):
            if not arg.startswith('-'):
                index = arg_i
                break

        # Unable to parse any arguments
        if index is None:
            return (args, None, [])

        return (args[:index], args[index], args[(index + 1):])

    def get_subcommands(self):
        return self.subcommands.itervalues()

    def print_help(self, cmd_name, args=None):
        # help <command>
        if cmd_name in self.subcommands:
            self.stream.print_command_usage(self.subcommands[cmd_name](self.stream))
            # if args[0] in self.subcommands:
            # else:
                # self.stream.print_basic_usage()
                # self.stream.write("ERROR: No command by the name %r" % (cmd_name,), colors.FAIL)

        else:
            self.stream.print_full_usage()

    def main(self, args):
        self.print_help()
        sys.exit(1)
