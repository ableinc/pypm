import os, io, subprocess, shlex, re
from .generator import Generator

generator = Generator()

def _update_package_json(pkgjson, path):
    generator.set_variables(path, False)
    generator.__writer__(pkgjson)


def update_package_json_after_operation(dependency, path, pkgjson):
    obj =  {}
    count = 2
    errors = []
    command = shlex.split(f'pip freeze')
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, env=os.environ.copy(), stderr=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding='utf8', newline=''):
        if dependency in line:
            en_v = re.sub("['\"]", '', line.replace('\n', ''))
            if en_v.find('>') == -1:
                idx = en_v.find('=')
            else:
                idx = en_v.find('>')
            obj[re.sub('\s+', '', str(en_v[:idx]))] = str(en_v[idx+count:])
    try:
        pkgjson['dependencies'].update(obj)
    except KeyError:
        pkgjson['devDependencies'].update(obj)
    except TypeError as te:
        print(f'Error occurred updating package.json. {dependency} was not found.')
        errors.append(te)
    finally:
        if len(errors) == 0:
            _update_package_json(pkgjson, path)


def update_package_json_after_uninstall(dependency, path, pkgjson):
    errors = []
    try:
        pkgjson['dependencies'][str(dependency)]
        del pkgjson['dependencies'][str(dependency)]
    except KeyError:
        del pkgjson['devDependencies'][str(dependency)]
    except TypeError as te:
        print(f'Error occurred updating package.json. {dependency} was not found.')
        errors.append(te)
    finally:
        if len(errors) == 0:
            _update_package_json(pkgjson, path)
        

