# pypm
Pure python package manager for Python 3 and above, similar to npm. This command line tool works just like npm and should mirror
its features. Python has no community adopted approach to managing projects. Also, outside of requirements.txt
there is no adopted approach to storing and maintaining dependencies. pyPM is the tool to adopt these community
requirements. It uses the same package.json structure as NPM, with all the configurations setup.py offers.

# Install
```bash
python3 setup.py install
```

# How to Use
pyPM works just like npm. You are granted the same operations such as, init, install, uninstall, update, start, and run.
Run:
```bash 
pypm --help
```

# Examples
1. init
    Generate a brand new package.json file from information in your requirements.txt and setup.py.
    ```bash
    pypm init
    ```
2. run
    Run a predefined scripts from the 'scripts' section of your package.json.
    ```bash
    pypm run tests
    ```
3. start
    Run the start script.
    ```bash
    pypm start
    ```
4. install <sup>1</sup>
    Install all or specific packages. Using 'install' as a standalone, it will install all dependencies listed in your package.json (if exists).
    ```bash
    pypm install
    ```
    or
    ```bash
    pypm install ***package1, package2***
    ```
5. uninstall <sup>1</sup>
    Uninstall all or specific packages. Using 'uninstall' as a standalone, it will uninstall all dependencies listed in your package.json (if exists).
    ```bash
    pypm uninstall
    ```
    or
    ```bash
    pypm uninstall ***package1, package2***
    ```
6. update <sup>1</sup>
    Update all or specific packages. Using 'update' as a standalone, it will update all dependencies listed in your package.json (if exists).
    ```bash
    pypm update
    ```
    or
    ```bash
    pypm update ***package1, package2***
    ```

# Key
<sup>1</sup> Any arguments that pip or npm allow can be combined into these command line arguments. Defined by adding -a/--arguments and entering arguments as such: [--no-cache, --upgrade]. NOTE: You MUST surround the arguments in brackets, it will fail it not.

# Notes
Documentation is on-going, so refer to examples above for now.

# Up Next
1. No cache options when installing. - Done | You may add any arguments that are allowed for pip or npm
2. Better automation algorithm when generating a new package.json
3. Possible PyPI easy install
