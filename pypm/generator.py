import json, re
import os.path


class Generator:
    """
        This class is called to generate a package.json for a given python project.
        The package.json is structured similar to npm's package.json. It will try
        to fetch information from requirements.txt and setup.py. If neither are
        present the generator will terminate.
    """
    def __init__(self, path, verbose, service):
        self.path = path
        self.verbose = verbose
        self.service = service

    def __writer__(self, data):
        with open(os.path.join(self.path, 'package2.json'), 'w', encoding='utf8') as packagejson:
            data = json.dumps(data, indent=4, ensure_ascii=True)
            packagejson.write(data)
    
    def __reader__(self, filename, datatype=None):
        with open(os.path.join(self.path, filename), 'r', encoding='utf8') as reader:
            if datatype is None:
                return reader.readlines()
            elif datatype == 'json':
                return json.loads(reader.read())

    def __organize_requirements__(self, req_file, count=2):
        obj = {}
        for env in req_file:
            en_v = re.sub("['\"]", '', env.replace('\n', ''))
            idx = en_v.find('=')
            obj[re.sub('\s+', '', str(en_v[:idx]))] = str(en_v[idx+count:])
        return obj
    
    def __get_user_input__(self):
        obj = {
            'scripts': {}
        }
        print('Press press enter to leave as default.\n')
        questions = [
            'Enter version (default: 0.0.1) > ',
            'Enter entry point file (default: blank) > ',
            'Enter start script (default: blank) > ',
            'Enter test script (default: npm default) > ',
            'Enter license (default: blank) > '
        ]
        for index, question in enumerate(questions):
            answer = input(question)
            if index == 0:
                obj['version'] = answer if answer != '' else '0.0.1'
            elif index == 1:
                obj['main'] = answer
            elif index == 2:
                obj['scripts']['start'] = answer
            elif index == 3:
                obj['scripts']['test'] = answer
            elif index == 4:
                obj['license'] = answer
        return obj
            
    def generate(self):
        if self.verbose:
            print('Running automated data retrieval tool. One moment...\n')
        req_dependencies = self.__organize_requirements__(self.__reader__('requirements.txt'))
        valid_meta = []
        for line in self.__reader__('setup.py'):
            for keyword in ['name', 'author', 'description', 'url', 'version']:
                # keyword = r'\b{}\d+\$'.format(keyword)
                if re.search(keyword + '=', line):
                    valid_meta.append(re.sub("['\"]", '', line.replace(',', '').replace('\n', '')))
        setup_py = self.__organize_requirements__(valid_meta, 1)
        template_package_json = self.__reader__('pypm/data/pkg.json', 'json')
        template_package_json['name'] = setup_py['name']
        template_package_json['version'] = setup_py['version']
        template_package_json['description'] = setup_py['description']
        template_package_json['dependencies'].update(req_dependencies)
        template_package_json['author'] = setup_py['author']
        if self.verbose:
            print('Automated data retrieval complete. Please follow on screen instructions below.\n')
        template_package_json.update(self.__get_user_input__())
        if self.verbose:
            print('Writing package.json...')
            print('Write to file complete.')
        self.__writer__(template_package_json)