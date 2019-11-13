import json, shlex, subprocess, io, sys
import os.path


class PyPM:
    def __init__(self, path, verbose, service):
        self.path = path
        self.verbose = verbose
        self.service = service
        self.package_json = None

    def __reader__(self):
        with open(os.path.join(self.path, 'package.json'), 'r', encoding='utf8') as packagejson:
            return json.loads(packagejson.read())

    def __commander__(self, key, item, arguments):
        arguments = arguments if arguments != None else ''
        option = {
            'run': shlex.split(item),
            'install': shlex.split(f'{self.service} install {arguments} {item}'),
            'uninstall': shlex.split(f'{self.service} uninstall {arguments} {item}'),
            'update': shlex.split(f'{self.service} install --upgrade {item}') if 'pip' in self.service else shlex.split(f'{self.service} update {arguments} {item}')
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
            print(f'Running command(s) {key}...\n')
        cmd = self.__commander__('run', str(self.package_json['scripts'][str(key)]))
        self.__process__(cmd)
    
    def install(self, key, arguments=None):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            self.__assign_package_json__()
            if self.verbose:
                print('Installilng all dependencies...')
            cmd = self.__commander__('install', self.__get_dependencies__(), arguments)
        else:
            if self.verbose:
                print(f'Installing package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('install', key, arguments)
        self.__process__(cmd)
    
    def uninstall(self, key, arguments=None):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            self.__assign_package_json__()
            if self.verbose:
                print('Uninstalling all dependencies...\n')
            cmd = self.__commander__('uninstall', self.__get_dependencies__(), arguments)
        else:
            if self.verbose:
                print(f'Uninstalling package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('uninstall', key, arguments)
        self.__process__(cmd)
    
    def update(self, key, arguments=None):
        key = self.__list_to_str__(key)
        if key.isspace() != False:
            self.__assign_package_json__()
            if self.verbose:
                print('Updating all dependencies...\n')
            cmd = self.__commander__('update', self.__get_dependencies__(), arguments)
        else:
            if self.verbose:
                print(f'Updating package(s) {self.__pretty_key__(key)}...\n')
            cmd = self.__commander__('update', key, arguments)
        self.__process__(cmd)
