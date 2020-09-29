import os.path as path
import os, json
import setuptools
from .errors import SetuptoolFailure
import io, shlex, subprocess, configparser, pkg_resources


class SetupGenerator:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def prereqs(self):
        cmd = shlex.split('python3 -m pip install --upgrade pip setuptools wheel')
        proc = subprocess.PIPE(stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line.replace('\n', ''))
        
    def set_generator_var(self, pkg_json):
        self.pkg_json = pkg_json
    
    def read(self):
        resource_package = __name__
        resource_path = '/'.join(('data', 'setup.cfg'))
        cfg = pkg_resources.resource_string(resource_package, resource_path).decode('utf-8')
        self.config.read_string(cfg)

    def write(self):
        with open('setup.cfg', 'w') as configfile:
            self.config.write(configfile)

    def _custom_key_(self, root_key, vkey):
        package_data_string = ''
        if vkey == 'package_data':
            for key, value in self.pkg_json[vkey]:
                if isinstance(value, list):
                    for vkey in value:
                        package_data_string += f'{key} = {value}'
                else:
                    package_data_string += f'{key} = {value}'
        else:
            self.config[root_key] = self.pkg_json[vkey]
    
    def _custom_key_join(self, root_key, vkey):
        self.config[root_key][vkey] = '\n'.join(self.pkg_json[vkey])
    
    def generate(self):
        content = {
            'metadata': ['name', 'version', 'description', 'long_description', 'keywords',
                'license', 'classifiers'],
            'options': ['zip_safe', 'include_package_data', 'package.dir',
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
                    else:
                        self.config[key][vkey] = self.pkg_json[vkey]
                except KeyError as ke:
                    print(ke)


class Setup(SetupGenerator):
    def __init__(self):
        super(SetupGenerator, self).__init__()
        self.pkg_json = None
        self.long_description = self._blank_setup_dict()
    
    def _remove_empty_values(self):
        for key, value in self.setup_dict.items():
            if value == None and key != 'packages':
                del self.setup_dict[key]
        
    def _config(self):
        self.pkg_json['setup']['entry_points'] = f"""{self.pkg_json['setup']['entry_points']}"""
        self.pkg_json['setup']['version'] = self.pkg_json['version']
        self.setup_dict.update(self.pkg_json['setup'])

    def set_vars(self, pkg_json):
        self.pkg_json = pkg_json
    
    def begin(self):
        # self._remove_empty_values()
        try:
            self.set_generator_var(self.pkg_json['setup'])
            self.prereqs()
            self.read()
            self.generate()
            self.write()
            setuptools.setup()
        except Exception as e:
            raise SetuptoolFailure(f'{e}')
