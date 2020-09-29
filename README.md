# pypm
Python package manager for Python 3, similar to npm. This command line tool works just like npm and should mirror its features. Python has no community adopted approach to managing projects. Also, outside of requirements.txt there is no adopted approach to storing and maintaining dependencies. In an effort to resolve this, I've introduced the pyPM tool. It uses the same package.json structure as npm, with all the configurations setup.py offers.

This project intends not to replace (npm) for Node, but to introduce the same project management features to the Python community. 

# Install
**requires Python 3.6**

PyPI
```bash
pip install pypm2
```
Locally
```bash
git clone https://github.com/ableinc/pypm.git
cd pypm
pip install --no-cache .
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
    pypm install package1 package2
    ```
5. uninstall <sup>1</sup><br />
    Uninstall all or specific packages. Using 'uninstall' as a standalone, it will uninstall all dependencies listed in your package.json (if exists).
    ```bash
    pypm uninstall
    ```
    or
    ```bash
    pypm uninstall package1 package2
    ```
6. update <sup>1</sup><br />
    Update all or specific packages. Using 'update' as a standalone, it will update all dependencies listed in your package.json (if exists).
    ```bash
    pypm update
    ```
    or
    ```bash
    pypm update package1 package2
    ```
7. setup<br />
    Instead of using setup.py, you can add the same arguments under the 'setup' key in the package.json, then run pypm setup to install your project. Later updates will include the ability to upload to PyPI using pypm.
    ```bash
    pypm setup
    ```

# Key
<sup>1</sup> Any arguments that pip or npm allow can be combined into these command line arguments. Initiated by adding --arguments option. Example:
```python
pypm install pydotenvs --no-cache
```
The above example will install the library pydotenvs via PyPI using Pip's built in --no-cache feature.

# Notes
1. Documentation is on-going, so refer to examples above for now.

2. Unfortunately someone beat me to the name pypm. Note that when you use pip install be sure to include the 2. This would normally be an issue if you imported this package, but it's a command line tool

3. When installing using npm, the package.json will not update dependencies. This is a known bug. Until fixed, use npm/npx to do your installing for node projects. All other features work.

4. When generating a setup.cfg file for development mode installation pip, setuptools and wheel
will be updated forecfully. You cannot opt out of this as the latest of setuptools is required
to build.

# Changelog
**September 2020**
Verbose is no longer default
Setup.py functionality added to package.json
Custom error messages
CLI updates

**August 2020**
CLI has been rebuilt; less complex.
PyPI easy install;  pip install pypm2

# Up Next
1. No cache options when installing. - ***Done*** | You may add any arguments that are allowed for pip or npm
2. Better automation algorithm when generating a new package.json - ***Done***
3. Possible PyPI easy install - ***Done***
4. Add package-lock.json - **currently in development**
5. Replace setup.py, move functionality to package.json - ***Done***
6. PyPI upload built in ***currently in development**
