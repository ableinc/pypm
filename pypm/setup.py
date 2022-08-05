import os.path as path
import os, json, sys, time
from .errors import SetuptoolFailure, NoSetupConfiguration
import io, shlex, subprocess, configparser, pkg_resources


class SetupGenerator:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def prereqs(self, python_version):
        cmd = shlex.split('{} -m pip install --upgrade pip setuptools wheel'.format(python_version))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line.replace('\n', ''))
        
    def set_generator_var(self, pkg_json):
        self.pkg_json = pkg_json
    
    def _get_package_resource(self, resource):
        resource_package = __name__
        resource_path = '/'.join(('data', resource))
        return pkg_resources.resource_string(resource_package, resource_path).decode('utf-8')

    def read(self):
        cfg = self._get_package_resource('setup.cfg')
        self.config.read_string(cfg)

    def write(self):
        setup_py = self._get_package_resource('setup.py')
        with open('setup.py', 'w') as setup_py_file:
            setup_py_file.write(setup_py)

        with open('setup.cfg', 'w') as configfile:
            self.config.write(configfile)

    def _custom_key_(self, root_key, vkey):
        package_data_string = ''
        if vkey == 'package_data':
            for key, value in self.pkg_json[vkey].items():
                list_to_str = '\n'.join(value)
                package_data_string += f"{key} = {list_to_str}"
        else:
            self.config[root_key] = self.pkg_json[vkey]
    
    def _custom_key_join(self, root_key, vkey):
        self.config[root_key][vkey] = '\n'.join(self.pkg_json[vkey])
    
    def generate(self):
        content = {
            'metadata': ['name', 'author', 'author_email', 'version', 'description', 'long_description', 'url', 'keywords',
                'license', 'classifiers', 'long_description_content_type'],
            'options': ['zip_safe', 'include_package_data', 'package_dir',
                'packages', 'scripts', 'install_requires', 'entry_points'],
            'options.package_data': ['package_data'],
            'options.extras_require': [],
            'options.packages.find': ['packages'],
            'options.data_files': ['data_files']
        }
        for key, value_keys in content.items():
            for vkey in value_keys:
                try:
                    if vkey == 'classifiers' or vkey == 'data_files' or vkey == 'keywords' or vkey == 'install_requires':
                        self._custom_key_join(key, vkey)
                    elif vkey == 'package_data':
                        self._custom_key_(key, vkey)
                    elif vkey == 'packages' and self.pkg_json['packages'] == []:
                        # if packages aren't specified, let setuptools find automatically
                        pass
                    elif key == 'options.packages.find' and self.pkg_json['package_dir']:
                        self.config[key]['where'] = self.pkg_json['package_dir'].replace('=', '')
                    else:
                        self.config[key][vkey] = self.pkg_json[vkey]
                except KeyError as ke:
                    if 'scripts' in str(ke):
                        del self.config['options']['scripts']
                    
                    if 'package_dir' in str(key):
                        del self.config['options']['package_dir']
                except TypeError:
                    pass

    
    def run_setup(self, python_version):
        cmd = shlex.split('{} -m pip install .'.format(python_version))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line.replace('\n', ''))


class Setup:
    def __init__(self):
        self.pkg_json = None
        self.generator = SetupGenerator()
        self.python_version = 'python3'

    def configure(self):
        try:
            self.pkg_json['setup']['name'] = self.pkg_json['name']
            self.pkg_json['setup']['license']  = self.pkg_json['license']
            self.pkg_json['setup']['version'] = self.pkg_json['version']
            self.pkg_json['setup']['author'] = self.pkg_json['author']
            self.pkg_json['setup']['description'] = self.pkg_json['description']
        except KeyError as ke:
            raise NoSetupConfiguration(ke)
        
        try:
            install_requires = []
            for dependency, version in self.pkg_json['dependencies'].items():
                install_requires.append(f'{dependency}=={version}')
            self.pkg_json['setup']['install_requires'] = install_requires
        except KeyError as ke:
            pass

    def set_vars(self, pkg_json, update_packages, python_version = 'python3'):
        self.pkg_json = pkg_json
        self.update_packages = update_packages
        self.python_version = python_version
    
    def begin(self):
        try:
            self.generator.set_generator_var(self.pkg_json['setup'])
            if self.update_packages:
                self.generator.prereqs(self.python_version)
            self.generator.read()
            self.generator.generate()
            self.generator.write()
            print('Awaiting setup...')
            time.sleep(3)
            self.generator.run_setup(self.python_version)
            print('Setup complete.')
        except Exception as e:
            raise SetuptoolFailure(str(e))
