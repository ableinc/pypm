import json, shlex, subprocess, io, sys, os
import os.path
from .post_operations import update_package_json_after_uninstall, update_package_json_after_operation
from .setup import Setup

cur_path = str(os.getcwd())
setuptool = Setup()

class PyPM:
    def __init__(self):
        self.package_json = None

    def set_variables(self, path=cur_path, verbose=False, service='pip', arguments=None):
        def args():
            return ' '.join(arguments.split(','))
        self.path = path
        self.verbose = verbose
        self.service = service
        self.arguments = [args() if arguments != None and ',' in arguments else arguments][0]

    def __reader__(self):
        try:
            with open(os.path.join(self.path, 'package.json'), 'r', encoding='utf8') as packagejson:
                return json.loads(packagejson.read())
        except FileNotFoundError:
            print('No package.json found. Please run pypm init')
            exit()

    def __commander__(self, key, item):
        arguments = self.arguments if self.arguments != None else ''
        option = {
            'run': shlex.split(f'{item} {arguments}'),
            'install': shlex.split(f'{self.service} install {arguments} {item}'),
            'uninstall': shlex.split(f'{self.service} uninstall {arguments} {item}'),
            'update': shlex.split(f'{self.service} install --upgrade {item}') if 'pip' in self.service else shlex.split(f'{self.service} update {arguments} {item}')
        }.get(key)
        return option

    def __get_dependency_version__(self, temp_dependency_list, dependency_list):
        final_dependency_list = list()
        for key in temp_dependency_list:
            final_dependency_list.append(f'{key}=={self.package_json[dependency_list][key]}')
        return final_dependency_list
    
    def __get_dependencies__(self, update=False):
        dependencies = list()
        hasErrors = False
        try:
            if update:
                dependencies = list(self.package_json['dependencies'].keys()).extend(list(self.package_json['devDependencies']).keys())
            else:
                temp_list_one = list(self.package_json['dependencies'].keys())
                dependencies = self.__get_dependency_version__(temp_list_one, 'dependencies')
                temp_list_two = list(self.package_json['devDependencies'].keys())
                dependencies.extend(self.__get_dependency_version__(temp_list_two, 'devDependencies'))
        except KeyError as ke:
            if ke == 'devDependencies':
                if update:
                    dependencies = list(self.package_json['dependencies'].keys())
                else:
                    temp_list_three = list(self.package_json['dependencies'].keys())
                    dependencies = self.__get_dependency_version__(temp_list_three, 'dependencies')
            else:
                hasErrors = True
        finally:
            if not hasErrors:
                return self.__list_to_str__(dependencies)
            print('No dependencies found.')
            sys.exit() 

    def __process__(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line.replace('\n', ''))

    def __list_to_str__(self, item_list):
        return ' '.join(item_list)

    def __pretty_key__(self, key):
        return key.replace(' ', ', ')
    
    def __assign_package_json__(self):
        self.package_json = self.__reader__()

    def start(self):
        self.__assign_package_json__()
        if self.verbose:
            print('Running start command...\n')
        cmd = self.__commander__('run', str(self.package_json['scripts']['start']))
        self.__process__(cmd)
    
    def run(self, key):
        self.__assign_package_json__()
        if self.verbose:
            print(f'Running {key}...\n')
        cmd = self.__commander__('run', str(self.package_json['scripts'][str(key)]))
        self.__process__(cmd)
    
    def install(self, key):
        key = self.__list_to_str__(key)
        self.__assign_package_json__()
        if len(key) == 0:
            if self.verbose:
                print('Installilng all dependencies...')
            cmd = self.__commander__('install', self.__get_dependencies__())
        else:
            if self.verbose:
                print(f'Installing package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('install', key)
        self.__process__(cmd)
        if len(key) != 0:
            update_package_json_after_operation(key, self.path, self.package_json)
    
    def uninstall(self, key):
        key = self.__list_to_str__(key)
        self.__assign_package_json__()
        if len(key) == 0:
            if self.verbose:
                print('Uninstalling all dependencies...\n')
            cmd = self.__commander__('uninstall', self.__get_dependencies__())
        else:
            if self.verbose:
                print(f'Uninstalling package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('uninstall', key)
        self.__process__(cmd)
        if len(key) != 0:
            update_package_json_after_uninstall(key, self.path, self.package_json)
    
    def update(self, key):
        key = self.__list_to_str__(key)
        self.__assign_package_json__()
        if len(key) == 0:
            if self.verbose:
                print('Updating all dependencies...\n')
            cmd = self.__commander__('update', self.__get_dependencies__(update=True))
        else:
            if self.verbose:
                print(f'Updating package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('update', key)
        self.__process__(cmd)
        if len(key) != 0:
            update_package_json_after_operation(key, self.path, self.package_json)
    
    def setup_py(self, key, python_version = 'python3'):
        self.__assign_package_json__()
        setuptool.set_vars(pkg_json=self.package_json, update_packages=key, python_version=python_version)
        setuptool.configure()
        setuptool.begin()
