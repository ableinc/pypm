import json, shlex, subprocess, io
import os.path


class PyPM:
    def __init__(self, path, verbose):
        self.path = path
        self.verbose = verbose
        self.package_json = self.__opener__()
    
    def __opener__(self):
        with open(os.path.join(self.path, 'package.json'), 'r', encoding='utf8') as packagejson:
            return json.loads(packagejson.read())

    def __commander__(self, key, item):
        option = {
            'run': shlex.split(item),
            'install': shlex.split(f'npm install {item}'),
            'uninstall': shlex.split(f'npm uninstall {item}'),
            'update': shlex.split(f'npm update {item}')
        }.get(key)
        return option

    def __process__(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            if self.verbose:
                print(line)

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
        if self.verbose:
            print(f'Installing package(s) {key}...\n')
        cmd = self.__commander__('install', str(key))
        self.__process__(cmd)
    
    def uninstall(self, key):
        if self.verbose:
            print(f'Uninstalling package(s) {key}...\n')
        cmd = self.__commander__('uninstall', str(key))
        self.__process__(cmd)
    
    def update(self, key):
        if self.verbose:
            print(f'Updating package(s) {key}...\n')
        cmd = self.__commander__('update', str(key))
        self.__process__(cmd)


