import sys, os, click, io, subprocess, shlex
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
        error_message = '[!] Error [!] Invalid service: ' + arg
        print(error_message)
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
        click.echo(f'Failed to generate package.json. Error: {e}')

@cli.command()
def getreqs():
    try:

        command = shlex.split('pip freeze > requirements.txt')
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(os.getcwd() + '/requirements.txt', 'w') as requirements:
            requirements.writelines(io.TextIOWrapper(proc.stdout, encoding='utf8').readlines())
    except Exception as e:
        click.echo(e)

@cli.command()
@click.argument('script')
def run(script):
    try:
        pypm.run(script)
    except Exception as e:
        click.echo(f'Script not found. Error: {e}')

@cli.command()
def start():
    try:
        pypm.start()
    except Exception as e:
        click.echo(f'Failed to run start script. Error: {e}')

@cli.command()
@click.argument('dependency', nargs=-1)
def install(dependency):
    try:
        pypm.install(dependency)
    except Exception as e:
        click.echo(f'Failed to install one or more dependencies. Error: {e}')

@cli.command()
@click.argument('dependency', nargs=-1)
def uninstall(dependency):
    try:
        pypm.uninstall(dependency)
    except Exception as e:
        click.echo(f'Failed to uninstall one or more dependencies. Error: {e}')

@cli.command()
@click.argument('dependency', nargs=-1)
def update(dependency):
    try:
        pypm.update(dependency)
    except Exception as e:
        click.echo(f'Failed to update one or more dependencies. Error: {e}')

@cli.command()
@click.argument('dependency', nargs=1, default=False)
@click.option('--python', type=str, default='python3', help='Specify which version of python to use. Default: python3')
def setup(dependency, python):
    try:
        pypm.setup_py(dependency, python)
    except Exception as e:
        click.echo(f'Failed to setup project. Error: {e}')


if __name__ == '__main__':
    cli()
