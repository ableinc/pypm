import json, re, os, sys, subprocess, io, shlex
import os.path, pkg_resources
from stdlib_list import stdlib_list

class Generator:
    """
        This class generates a package.json for a given python project.
        The package.json is structured similar to npm's package.json. It will try
        to fetch information from requirements.txt and setup.py. If neither are
        present the generator will terminate.
    """
    def __init__(self):
        self.path = str(os.getcwd())
        self.verbose = True
        self.valid_version = True
        self.default_packages = stdlib_list(f'{sys.version[0:3]}')
        self.self_generated_reqs = False

    def set_variables(self, path, verbose):
        self.path = path
        self.verbose = verbose

    def __writer__(self, data):
        with open(os.path.join(self.path, 'package.json'), 'w', encoding='utf8') as packagejson:
            data = json.dumps(data, indent=4, ensure_ascii=True)
            packagejson.write(data)
    
    def __reader__(self, filename, datatype=None):
        try:
            with open(os.path.join(self.path, filename), 'r', encoding='utf8') as reader:
                if datatype is None:
                    return reader.readlines()
                elif datatype == 'json':
                    return json.loads(reader.read())
        except FileNotFoundError:
            # print(f'{filename} Not Found. Please ensure you have both setup.py and requirements.txt in your root directory.')
            return None

    def __organize_requirements__(self, req_file, count=2):
        obj = {}
        for env in req_file:
            en_v = re.sub("['\"]", '', env.replace('\n', ''))
            if en_v.find('>') == -1:
                idx = en_v.find('=')
            else:
                idx = en_v.find('>')
            obj[re.sub('\s+', '', str(en_v[:idx]))] = str(en_v[idx+count:])
        return obj
    
    def __get_user_input__(self, no_setup_py=False):
        obj = {
            'scripts': {}
        }
        print('Press press enter to leave as default.\n')
        if no_setup_py:
            questions = [
                f'Enter name of project (default: {os.path.basename(self.path)}) > ',
                'Enter version (default: 0.0.1) > ',
                'Enter description (default: blank) > ',
                'Enter author (default: blank) > ',
                'Enter entry point file (default: main.py) > ',
                'Enter start script (default: python [entry point file]) > ',
                'Enter test script (default: blank) > ',
                'Enter license (default: ISC) > '
            ]
            for index, question in enumerate(questions):
                answer = input(question)
                if index == 0:
                    obj['name'] = answer if answer != '' else f'{os.path.basename(self.path)}'
                elif index == 1:
                    obj['version'] = answer if answer != '' else '0.0.1'
                elif index == 2:
                    obj['description'] = answer if answer != '' else ''
                elif index == 3:
                    obj['author'] = answer if answer != '' else ''
                elif index == 4:
                    if answer == '':
                        obj['main'] = 'main.py'
                    obj['main'] = answer if answer != '' else f"{obj['main']}"
                elif index == 5:
                    obj['scripts']['start'] = answer if answer != '' else f"python {obj['main']}"
                elif index == 6:
                    obj['scripts']['test'] = answer if answer != '' else 'echo "No test available"'
                elif index == 7:
                    obj['license'] = answer if answer != '' else 'ISC'
        else:
            questions = [
                'Enter version (default: 0.0.1) > ',
                'Enter entry point file (default: main.py) > ',
                'Enter start script (default: python [entry point file]) > ',
                'Enter test script (default: blank) > ',
                'Enter license (default: ISC) > '
            ]
            for index, question in enumerate(questions):
                answer = input(question)
                if index == 0:
                    obj['version'] = answer if answer != '' else '0.0.1'
                elif index == 1:
                    if answer == '':
                        obj['main'] = 'main.py'
                    obj['main'] = answer if answer != '' else f"{obj['main']}"
                elif index == 2:
                    obj['scripts']['start'] = f"python {obj['main']}" if answer != '' else "python main.py"
                elif index == 3:
                    obj['scripts']['test'] = answer if answer != '' else 'echo "No test available"'
                elif index == 4:
                    obj['license'] = answer if answer != '' else 'ISC'
        return obj
        
    
    def __check_file_system__ (self, filename):
        if os.path.isfile(os.path.join(self.path, 'package.json')):
            print('package.json already exists for this project.')
            exit()
        else:
            if not os.path.isfile(os.path.join(self.path, filename)):
                try:
                    command = shlex.split('pip freeze > requirements.txt')
                    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    with open(os.getcwd() + '/requirements.txt', 'w') as requirements:
                        requirements.writelines(io.TextIOWrapper(proc.stdout, encoding='utf8').readlines())
                    self.self_generated_reqs = True
                except Exception:
                    print('Unable to generate requirements.txt. Run: pypm getreqs - to create the requirements.txt file')
                    exit()

    def _create_structure_(self, setup_py, template_package_json, req_dependencies):
        template_package_json['name'] = setup_py['name']
        template_package_json['version'] = setup_py['version']
        if '.' not in setup_py['version']:
            self.valid_version = False
        template_package_json['description'] = setup_py['description']
        template_package_json['dependencies'].update(req_dependencies)
        template_package_json['author'] = setup_py['author']
        return template_package_json
    
    def generate(self):
        if self.verbose:
            print('Running automated data retrieval tool. One moment...')
        self.__check_file_system__('requirements.txt')
        req_dependencies = self.__organize_requirements__(self.__reader__('requirements.txt'))
        setup_py_contents = self.__reader__('setup.py')
        resource_package = __name__
        resource_path = '/'.join(('data', 'pkg.json'))
        template = pkg_resources.resource_string(resource_package, resource_path).decode('utf-8')
        template_package_json = json.loads(template)
        valid_meta = []
        noSetupPy = False
        if setup_py_contents is not None:
            for line in setup_py_contents:
                for keyword in ['name', 'author', 'description', 'url', 'version']:
                    if re.search(keyword + '=', line):
                        valid_meta.append(re.sub("['\"]", '', line.replace(',', '').replace('\n', '')))
            setup_py = self.__organize_requirements__(valid_meta, 1)
            template_package_json = self._create_structure_(setup_py, template_package_json, req_dependencies)
        else:
            noSetupPy = True
        if self.verbose:
            print('Automated data retrieval complete. Please follow on screen instructions below.\n')
        template_package_json.update(self.__get_user_input__(no_setup_py=noSetupPy))
        if self.verbose:
            print('Writing package.json...')
            print('Write to file complete.')
        self.__writer__(template_package_json)
        if self.self_generated_reqs:
            os.remove(os.path.join(self.path, 'requirements.txt'))
