import commands


def sh(cmd, *args):
    if args:
        line = cmd % tuple(args)
    else:
        line = cmd
    return commands.getoutput(line)
