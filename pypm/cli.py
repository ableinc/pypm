import argparse, sys, os
try:
    from version import __version__
    from main import PyPM
    from generator import Generator
except ImportError:
    from pypm.version import __version__
    from pypm.main import PyPM
    from pypm.generator import Generator


def service_check(arg):
    available_option = {
        'pip': True,
        'pip3': True,
        'npm': True
    }.get(arg, False)
    if available_option:
        return True
    else:
        print(f'[!] Error [!] Invalid service: {arg}')
        sys.exit(1)


def sanitize_arguments(arguments):
    if arguments == '' or arguments is None:
        return None
    output = []
    for arg in arguments.split(' '):
        if '[' in arg or ']' in arg:
            output.append(arg.replace('[', '').replace(']', ''))
    return ' '.join(output)


def cli(args):
    errors = False
    service_check(args.service)
    try:
        pypm = PyPM(args.path, args.verbose, args.service)
        generator = Generator(args.path, args.verbose, args.service)
    except FileNotFoundError as fn:
        print(f'[!] Error [!]\n: {fn}')
        sys.exit(1)
    finally:
        try:
            fetch = ''.join(args.run[0] if len(args.run) > 0 else args.run)
            valid_run = {
                'generate': generator.generate,
                'run': pypm.run,
                'start': pypm.start,
                'install': pypm.install,
                'uninstall': pypm.uninstall,
                'update': pypm.update,
            }.get(fetch, False)
            if valid_run and args.run[0] == 'start':
                valid_run()
            elif valid_run and args.run[0] == 'run':
                valid_run(args.run[1])
            elif valid_run and args.run[0] == 'generate':
                valid_run()
            elif valid_run:
                valid_run(args.run[1:], arguments=sanitize_arguments(args.arguments))
            elif args.version:
                print(__version__)
        except (TypeError, OSError, AttributeError) as eee:
            print(f'[!] Error [!]\n{eee}')
        except KeyError as ke:
            print(f'Could not find {ke} in package.json. Please confirm it is present.')
        except FileNotFoundError as fnfe:
            print(f'Could not find file.\n{fnfe}')
        finally:
            if errors:
                print('Error(s) occurred. Please refer above.')


def main():
    path = str(os.getcwd())
    parser = argparse.ArgumentParser(prog='pypm', description='Pure python package manager for Python 3 and above, similar to npm')
    parser.add_argument('-v', '--verbose', type=bool, default=True, help='Message output')
    parser.add_argument('-s', '--service', type=str, default='pip', help='Which service to use (pip, pip3 or npm)')
    parser.add_argument('-p', '--path', type=str, default=path, help='Path of package.json. Defaults to current directory CLI tool is called from.')
    parser.add_argument('-vv', '--version', type=bool, default=False, help='Get current version of pypm.')
    parser.add_argument('-a', '--arguments', type=str, default='', help='Add additional arguments to run with pip or npm.')
    parser.add_argument('run', nargs='*', type=str, default='')
    args = parser.parse_args()
    cli(args)


if __name__ == '__main__':
    main()
