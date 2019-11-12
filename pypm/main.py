import json, shlex, subprocess, io, sys
import os.path


class PyPM:
    def __init__(self, path, verbose, service):
        self.path = path
        self.verbose = verbose
        self.service = service
        self.package_json = self.__reader__()

    def __reader__(self):
        with open(os.path.join(self.path, 'package.json'), 'r', encoding='utf8') as packagejson:
            return json.loads(packagejson.read())

    def __commander__(self, key, item):
        option = {
            'run': shlex.split(item),
            'install': shlex.split(f'{self.service} install {item}'),
            'uninstall': shlex.split(f'{self.service} uninstall {item}'),
            'update': shlex.split(f'{self.service} install --upgrade {item}') if 'pip' in self.service else shlex.split(f'{self.service} update {item}')
        }.get(key)
        return option

    def __get_dependencies__(self):
        try:
            depends = list(self.package_json['dependencies'].keys())
            depends.extend(list(self.package_json['devDependencies'].keys()))
            return self.__list_to_str__(depends)
        except KeyError as ke:
            if ke == 'devDependencies':
                return self.__list_to_str__(list(self.package_json['dependencies'].keys()))
            else:
                print('No dependencies found.')
                sys.exit()

    def __process__(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            if self.verbose:
                print(line)

    def __list_to_str__(self, item_list):
        return ' '.join(item_list)

    def __pretty_key__(self, key):
        return key.replace(' ', ', ')
    
    def start(self):
        if self.verbose:
            print('Running start command...\n')
        cmd = self.__commander__('run', str(self.package_json['scripts']['start']))
        self.__process__(cmd)
    
    def run(self, key):
        if self.verbose:
            print(f'Running command(s) {key}...\n')
        cmd = self.__commander__('run', str(self.package_json['scripts'][str(key)]))
        self.__process__(cmd)
    
    def install(self, key):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            if self.verbose:
                print('Installilng all dependencies...')
            cmd = self.__commander__('install', self.__get_dependencies__())
        else:
            if self.verbose:
                print(f'Installing package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('install', key)
        self.__process__(cmd)
    
    def uninstall(self, key):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            if self.verbose:
                print('Uninstalling all dependencies...\n')
            cmd = self.__commander__('uninstall', self.__get_dependencies__())
        else:
            if self.verbose:
                print(f'Uninstalling package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('uninstall', key)
        self.__process__(cmd)
    
    def update(self, key):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            if self.verbose:
                print('Updating all dependencies...\n')
            cmd = self.__commander__('update', self.__get_dependencies__())
        else:
            if self.verbose:
                print(f'Updating package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('update', key)
        self.__process__(cmd)
