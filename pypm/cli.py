import argparse, sys, os, click
try:
    from version import __version__
    from main import PyPM
    from generator import Generator
except ImportError:
    from pypm.version import __version__
    from pypm.main import PyPM
    from pypm.generator import Generator

pypm = PyPM()
generator = Generator()

def service_check(arg):
    available_option = {
        'pip': True,
        'pip3': True,
        'npm': True
    }.get(arg, False)
    if not available_option:
        print(f'[!] Error [!] Invalid service: {arg}')
        sys.exit(1)


@click.group()
@click.option('--path', type=str, default=str(os.getcwd()), help='Path of package.json. Defaults to current directory CLI tool is called from.')
@click.option('--verbose', type=bool, default=True, help='Message output')
@click.option('--service', type=str, default='pip', help='Which service to use (pip, pip3 or npm)')
@click.option('--arguments', type=str, help='Extra pip or npm arguments to append to commands.')
def cli(path, verbose, service, arguments):
    """Python package manager for projects running Python3.6 and above."""
    service_check(service)
    pypm.set_variables(path, verbose, service, arguments)
    generator.set_variables(path, verbose)


@cli.command()
def init():
    try:
        generator.generate()
    except Exception:
        click.echo('You must invoke options to generate package.json')

@cli.command()
@click.argument('script')
def run(script):
    pypm.run(script)

@cli.command()
def start():
    pypm.start()

@cli.command()
@click.argument('dependency', nargs=-1)
def install(dependency):
    pypm.install(dependency)

@cli.command()
@click.argument('dependency', nargs=-1)
def uninstall(dependency):
    pypm.uninstall(dependency)

@cli.command()
@click.argument('dependency', nargs=-1)
def update(dependency):
    pypm.update(dependency)


@cli.command()
def version():
    click.echo(__version__)


if __name__ == '__main__':
    cli()
