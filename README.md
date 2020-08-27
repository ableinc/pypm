# pypm
Python package manager for Python 3, similar to npm. This command line tool works just like npm and should mirror its features. Python has no community adopted approach to managing projects. Also, outside of requirements.txt there is no adopted approach to storing and maintaining dependencies. In an effort to resolve this, I've introduced the pyPM tool. It uses the same package.json structure as npm, with all the configurations setup.py offers.

# Install
**requires Python 3.6**

```bash
pip install pypm2
```

# How to Use
pyPM works just like npm. You are granted the same operations such as, init, install, uninstall, update, start, and run.
Run:
```bash 
pypm --help
```

# Examples
1. init<br />
    Generate a brand new package.json file from information in your requirements.txt and setup.py.
    ```bash
    pypm init
    ```
2. run<br />
    Run a predefined scripts from the 'scripts' section of your package.json.
    ```bash
    pypm run tests
    ```
3. start<br />
    Run the start script.
    ```bash
    pypm start
    ```
4. install <sup>1</sup><br />
    Install all or specific packages. Using 'install' as a standalone, it will install all dependencies listed in your package.json (if exists).
    ```bash
    pypm install
    ```
    or
    ```bash
    pypm install ***package1 package2***
    ```
5. uninstall <sup>1</sup><br />
    Uninstall all or specific packages. Using 'uninstall' as a standalone, it will uninstall all dependencies listed in your package.json (if exists).
    ```bash
    pypm uninstall
    ```
    or
    ```bash
    pypm uninstall ***package1 package2***
    ```
6. update <sup>1</sup><br />
    Update all or specific packages. Using 'update' as a standalone, it will update all dependencies listed in your package.json (if exists).
    ```bash
    pypm update
    ```
    or
    ```bash
    pypm update ***package1 package2***
    ```

# Key
<sup>1</sup> Any arguments that pip or npm allow can be combined into these command line arguments. Defined by adding -a/--arguments and entering arguments as such: [--no-cache, --upgrade]. NOTE: You MUST surround the arguments in brackets, it will fail it not.

# Notes
Documentation is on-going, so refer to examples above for now.

Unfortunately someone beat me to the name pypm. Note that when you use pip install be sure to include the 2. This would normally be an issue if you imported this package, but it's a command line tool

# Changelog
**August 2020**
CLI has been rebuilt; less complex.
PyPI easy install;  pip install pypm2

# Up Next
1. No cache options when installing. - ***Done*** | You may add any arguments that are allowed for pip or npm
2. Better automation algorithm when generating a new package.json - ***Done***
3. Possible PyPI easy install - ***Done***
4. Add package-lock.json **currently in development**
