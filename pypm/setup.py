import os.path as path
import os, json, sys
from .errors import SetuptoolFailure, NoSetupConfiguration
import io, shlex, subprocess, configparser, pkg_resources


class SetupGenerator:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def prereqs(self):
        cmd = shlex.split('python3 -m pip install --upgrade pip setuptools wheel')
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
        if path.isfile('setup.cfg'):
            self.config.read('setup.cfg')
            return
        cfg = self._get_package_resource('setup.cfg')
        self.config.read_string(cfg)

    def write(self):
        setup_py = self._get_package_resource('_setup.py')
        with open('_setup.py', 'w') as setup_py_file:
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
            'metadata': ['name', 'version', 'description', 'long_description', 'keywords',
                'license', 'classifiers'],
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
                    elif vkey == 'packages' and self.pkg_json['packages'] == '':
                        # if packages aren't specified, let setuptools find automatically
                        pass
                    elif key == 'options.packages.find' and self.pkg_json['package_dir']:
                        self.config[key]['where'] = self.pkg_json['package_dir'].replace('\n', '').replace('=', '')
                    else:
                        self.config[key][vkey] = self.pkg_json[vkey]
                except KeyError as ke:
                    if 'scripts' in str(ke):
                        del self.config['options']['scripts']
                except TypeError as te:
                    print(f'TypeError: {te}')
    
    def run_setup(self):
        cmd = shlex.split('python install --editable .')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line.replace('\n', ''))


class Setup:
    def __init__(self):
        self.pkg_json = None
        self.generator = SetupGenerator()
    
    def setupCfgExists(self):
        if path.isfile('setup.cfg'):
            return True
        return False

    def configure(self):
        try:
            self.pkg_json['setup']['license']  = self.pkg_json['license']
            self.pkg_json['setup']['version'] = self.pkg_json['version']
        except KeyError as ke:
            raise NoSetupConfiguration(ke)
            sys.exit()

    def set_vars(self, pkg_json, update_packages):
        self.pkg_json = pkg_json
        self.update_packages = update_packages
    
    def begin(self):
        self.generator.set_generator_var(self.pkg_json['setup'])
        if self.update_packages:
            self.generator.prereqs()
        if not self.setupCfgExists():
            self.generator.read()
            self.generator.generate()
            self.generator.write()
        # self.generator.run_setup()
