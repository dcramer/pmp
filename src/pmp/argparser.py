import inspect
import sys


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def color_output(message, color=None):
    if color:
        output = color
    else:
        output = ""
    output += message
    output += colors.ENDC
    return output


class Argument(object):
    def __init__(self, name, var=None, help='', required=False, multiple=False):
        self.name = name
        self.var = var  # same as dest in optparse
        self.help = help
        self.required = required
        self.multiple = multiple

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

    def add_option(self, *args, **kwargs):
        self.parser.add_option(*args, **kwargs)

    def parse_args(self, argv):
        main_args, cmd_name, cmd_args = self.parse_subcommand(argv)
        if cmd_name is None or cmd_name == 'help':
            # TODO: 'help <command>'
            if cmd_args:
                if cmd_args[0] in self.subcommands:
                    self.stream.print_command_usage(self.subcommands[cmd_args[0]]())
                else:
                    self.stream.print_basic_usage()
                    self.stream.write("ERROR: No command by the name %r" % (cmd_name,), colors.FAIL)
            else:
                self.stream.print_full_usage()
            sys.exit(1)

        # Parser main options
        (main_options, _) = self.parser.parse_args(main_args)

        if cmd_name not in self.subcommands:
            self.stream.print_basic_usage()
            self.stream.write("ERROR: No command by the name %r" % (cmd_name,), colors.FAIL)
            sys.exit(1)
        command = self.subcommands[cmd_name]()

        # cmd_options, cmd_args = cmd_parser.parse_args(cmd_args)
        # return command, cmd_args, cmd_options.__dict__

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
