import argparse, sys, os, click
from .version import __version__
from .main import PyPM
from .generator import Generator

pypm = PyPM()
generator = Generator()

def service_check(arg):
    available_option = {
        'pip': True,
        'pip3': True,
        'npm': True,
        'npx': True
    }.get(arg, False)
    if not available_option:
        print(f'[!] Error [!] Invalid service: {arg}')
        sys.exit(1)


@click.group()
@click.option('--path', type=str, default=str(os.getcwd()), help='Path of package.json. Defaults to current directory CLI tool is called from.')
@click.option('--verbose', type=bool, default=False, help='Message output')
@click.option('--service', type=str, default='pip', help='Which service to use (pip, pip3, npm, npx)')
@click.option('--arguments', type=str, help='Extra pip, npm or npx arguments to append to commands.')
@click.version_option(version=__version__)
def cli(path, verbose, service, arguments):
    """Python package manager for projects running Python3.6 and above."""
    service_check(service)
    pypm.set_variables(path, verbose, service, arguments)


@cli.command()
@click.argument('path', nargs=1, default=os.getcwd())
@click.argument('verbose', nargs=1, default=False)
def init(path, verbose):
    try:
        generator.set_variables(path, verbose)
        generator.generate()
    except Exception as e:
        click.echo(f'Failed to generate package.json. Error: \n', e)


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
@click.argument('dependency', nargs=1, default=False)
def setup(dependency):
    pypm.setup_py(dependency)


if __name__ == '__main__':
    cli()
