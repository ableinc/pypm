import argparse, sys, os
try:
    from version import __version__
    from main import PyPM
except ImportError:
    from pypm.version import __version__
    from pypm.main import PyPM


def handler(arg, cli_tool):
    def run_start():
        cli_tool.start()
    if len(arg) == 1 and arg[0] == 'start':
        run_start()
        return False
    elif len(arg) == 2 and arg[0] == 'run':
        if arg[1] == 'start':
            run_start()
            return False
    return True

def cli(args):
    errors = False
    pypm = PyPM(args.path, args.verbose)

    try:
        if handler(args.run, pypm):
            pypm.run(args.run[1])
        elif args.install:
            pypm.install(args.install[1:])
        elif args.uninstall:
            pypm.uninstall(args.uninstall[1:])
        elif args.version:
            print(__version__)
        elif args.update:
            pypm.update(args.update[1:])
    except (TypeError, OSError, AttributeError) as eee:
        print(eee)
    except KeyError as ke:
        if args.verbose:
            print(f'Could not find {ke} in package.json. Please confirm it is present.')
    finally:
        if errors and args.verbose:
            print('Error(s) occurred. Please refer above.')


if __name__ == '__main__':
    path = str(os.getcwd())
    parser = argparse.ArgumentParser(prog='pypm', description='Npm like package manager for Python')
    parser.add_argument('-v', '--verbose', type=bool, default=True, help='Message output')
    parser.add_argument('run', nargs='+', type=str)
    parser.add_argument('install', nargs='*', type=str)
    # parser.add_argument('start', nargs='?', type=str, default=False)
    parser.add_argument('uninstall', nargs='*', type=str)
    parser.add_argument('update', nargs='*', type=str)
    parser.add_argument('version', nargs='?', type=bool, default=False)
    parser.add_argument('path', nargs='?', type=str, default=path)
    args = parser.parse_args()
    cli(args)
