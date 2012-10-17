import sys

from .argparser import CommandParser
from .commands import registry


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = CommandParser(registry)
    command, cmd_args, cmd_kwargs = parser.parse_args(argv)
    command.run(cmd_args, **cmd_kwargs)

if __name__ == '__main__':
    main()
