import sys
from run import run


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        raise ValueError('Must provide a command name.')
    if not len(args) == 2:
        raise ValueError('Must provide only one argument.')
    _, command_name = args
    if command_name == 'run':
        pass
    else:
        raise ValueError('No matching command.')
