# PyPM

Pypm is a python package manager for projects using Python 3 and above. This library is similar to npm. This command line tool works just like npm and should mirror its features.

## Reason

The python community has no package management tool that is closely maintained. Also, outside of requirements.txt there is no adopted approach to storing and maintaining dependencies. In an effort to change this, I've introduced the PyPM tool. It uses the same package.json structure as npm, with all the configurations setup.py offers.

This project does not intend to replace npm for NodeJS, but introduce the same project management features to the Python community.

## Install

***requires Python 3.6 or above***

PyPI

```bash
pip install pypm2
```

Locally

```bash
git clone https://github.com/ableinc/pypm
cd pypm
pip install --editable .
```

Visit PyPi:
[PyPi for Pyenv](https://pypi.org/project/pypm2/)

## How to Use

PyPM works just like npm. You are granted the same operations such as, init, install, uninstall, update, start, and run.
Run:

```bash
pypm --help
```

## Usage

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
    Instead of manually creating setup.py and setup.cfg files, you can add the same arguments under the 'setup' key in the package.json (refer to package.json), then run pypm setup to install your project locally.

    ```bash
    pypm setup
    ```

    Update setuptools, wheel, pip:

    ```bash
    pypm setup True
    ```

    Specify a version of python to use:

    ```bash
    pypm setup --python python3.9
    ```

8. getreqs<br />
    Generate the requirments.txt file based on your (virtual) environment.

    ```bash
    pypm getreqs
    ```

## Key

<sup>1</sup> Any arguments that pip or npm allow can be combined into these command line arguments. Initiated by adding --arguments option. Example:

```bash
pypm --arguments --no-cache install pydotenvs
```

The above example will install the library pydotenvs via PyPI using Pip's built in --no-cache feature.

If you have multiple arguments to append to a command you can seperate them by commas. For example:

```bash
pypm --arguments --no-cache,--verbose,--logs,~/Downloads install pydotenvs
```

## Notes

1. Documentation is on-going, so refer to examples above for now.

2. Unfortunately someone beat me to the name pypm. Note that when you use pip install be sure to include the 2. This would normally be an issue if you imported this package, but it's a command line tool

3. When installing using npm, the package.json will not update dependencies. This is a known bug. Until fixed, use npm/npx to do your installing for node projects. All other features work.

4. When generating the setup.py & setup.cfg files for development mode installation pip, setuptools and wheel may need to be updated. Follow the instructions above to update alongside setup functionality.

## Changelog

**August 2022**

- Updated how the package is installed on the system
- New algorithm for automatically generating the requirements.txt file has been added
- ```pypm init``` can now generate the requirements.txt file by pypm command (pypm getreqs)
- You can now specify a version of python to use for ```pypm setup```. By default it will use python3.

**June 2021**

- Enhanced the arguments feature for CLI tool.

**April 2021**

- Minor bug fix to CLI tool; version update.

**September 2020**

- Verbose is no longer default
- Setup.py functionality added to package.json
- Custom error messages
- CLI updates
***Setup.py feature  has been introduced in version 0.1.3***

**August 2020**

- CLI has been rebuilt; less complex.
- PyPI easy install;  pip install pypm2

## Up Next

1. No cache options when installing. - ***Done*** | You may add any arguments that are allowed for pip, npm or any other CLI tool arguments
2. Better automation algorithm when generating a new package.json - ***Done***
3. Possible PyPI easy install - ***Done***
4. Add package-lock.json - **currently in development**
5. Replace setup.py & setup.cfg, move functionality to package.json - ***Done***
6. PyPI upload built in ***Done***
