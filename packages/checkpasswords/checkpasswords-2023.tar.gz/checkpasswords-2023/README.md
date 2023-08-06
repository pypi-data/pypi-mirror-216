[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](../../)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/CheckPasswords.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/checkpasswords.svg?style=for-the-badge)](https://pypistats.org/packages/checkpasswords)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fcheckpasswords)](https://pepy.tech/project/CheckPasswords)
[![PyPI Version](https://img.shields.io/pypi/v/CheckPasswords.svg?style=for-the-badge)](https://pypi.org/project/CheckPasswords)

<!-- omit in toc -->
# CheckPasswords

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Uses pass_import to read a password manager source file storing raw data and infers data such as:

- zxcvbnScore
- isPasswordDuplicate
- passwordPrint
- isHttp
- isMfaAvailable
- isMfaEnabled

Used to:

- check for duplicate passwords
- check for weak passwords
- identify http sites
- list available 2fa options using data from https://2fa.directory/
- list emails to submit to HIBP or similar

<!-- omit in toc -->
## Table of Contents

- [Using](#using)
	- [CLI Help](#cli-help)
	- [Example Output](#example-output)
- [Documentation](#documentation)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Windows - Python.org](#windows---pythonorg)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
	- [Dnf](#dnf)
- [Install Python on MacOS](#install-python-on-macos)
	- [Homebrew](#homebrew)
	- [MacOS - Python.org](#macos---pythonorg)
- [How to run](#how-to-run)
	- [Windows](#windows)
	- [Linux/ MacOS](#linux-macos)
- [Download Project](#download-project)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)
	- [Support](#support)
	- [Rationale](#rationale)

## Using

### CLI Help

```txt
usage: __main__.py [-h] [--output-format OUTPUT_FORMAT] [--input-format INPUT_FORMAT] [--file FILE] [--no-colour]
                   credentials

checkpasswords: Uses pass_import to read a password manager source file storing raw
data and infers data such as:

- zxcvbnScore
- isPasswordDuplicate
- passwordPrint
- isHttp
- isMfaAvailable
- isMfaEnabled

Used to:

- check for duplicate passwords
- check for weak passwords
- identify http sites
- list available 2fa options using data from https://2fa.directory/
- list emails to submit to HIBP or similar

positional arguments:
  credentials           Credentials/ passwords file to check

options:
  -h, --help            show this help message and exit
  --output-format OUTPUT_FORMAT, -o OUTPUT_FORMAT
                        Output format. One of ['ansi', 'plain', 'markdown', 'json', 'raw', 'raw-csv']. default=ansi
  --input-format INPUT_FORMAT, -i INPUT_FORMAT
                        Input format. One of ['1password', 'aegis', 'andotp', 'apple-keychain', 'bitwarden', 'blur', 'buttercup', 'chrome', 'clipperz', 'csv', 'dashlane', 'encryptr', 'enpass', 'firefox', 'fpm', 'freeotp+', 'gnome', 'gnome-auth', 'gopass', 'gorilla', 'kedpm', 'keepass', 'keepassx', 'keepassx2', 'keepassxc', 'keeper', 'lastpass', 'myki', 'network-manager', 'padlock', 'pass', 'passman', 'passpack', 'passpie', 'pwsafe', 'revelation', 'roboform', 'saferpass', 'upm', 'zoho']
  --file FILE, -f FILE  Filename to write to (omit for stdout)
  --no-colour, -z       No ANSI colours
```

### Example Output

```txt

                Summary
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Issue               ┃ No. Instances ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Duplicate Passwords │ 2             │
│ Weak Passwords      │ 9             │
│ HTTP Sites          │ 9             │
│ Enable 2FA          │ 16            │
│ Emails              │ 17            │
└─────────────────────┴───────────────┘

...
```

## Documentation

A high-level overview of how the documentation is organized organized will help you know
where to look for certain things:

<!--
- [Tutorials](/documentation/tutorials) take you by the hand through a series of steps to get
  started using the software. Start here if you’re new.
-->
- The [Technical Reference](/documentation/reference) documents APIs and other aspects of the
  machinery. This documentation describes how to use the classes and functions at a lower level
  and assume that you have a good high-level understanding of the software.
<!--
- The [Help](/documentation/help) guide provides a starting point and outlines common issues that you
  may have.
-->

## Install With PIP

```python
pip install CheckPasswords
```

Head to https://pypi.org/project/CheckPasswords/ for more info

## Language information

### Built for

This program has been written for Python versions 3.8 - 3.11 and has been tested with both 3.8 and
3.11

## Install Python on Windows

### Chocolatey

```powershell
choco install python
```

### Windows - Python.org

To install Python, go to https://www.python.org/downloads/windows/ and download the latest
version.

## Install Python on Linux

### Apt

```bash
sudo apt install python3.x
```

### Dnf

```bash
sudo dnf install python3.x
```

## Install Python on MacOS

### Homebrew

```bash
brew install python@3.x
```

### MacOS - Python.org

To install Python, go to https://www.python.org/downloads/macos/ and download the latest
version.

## How to run

### Windows

- Module
	`py -3.x -m [module]` or `[module]` (if module installs a script)

- File
	`py -3.x [file]` or `./[file]`

### Linux/ MacOS

- Module
	`python3.x -m [module]` or `[module]` (if module installs a script)

- File
	`python3.x [file]` or `./[file]`

## Building

This project uses https://github.com/FHPythonUtils/FHMake to automate most of the building. This
command generates the documentation, updates the requirements.txt and builds the library artefacts

Note the functionality provided by fhmake can be approximated by the following

```sh
handsdown  --cleanup -o documentation/reference
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output requirements_optional.txt
poetry build
```

`fhmake audit` can be run to perform additional checks

## Testing

For testing with the version of python used by poetry use

```sh
poetry run pytest
```

Alternatively use `tox` to run tests over python 3.8 - 3.11

```sh
tox
```

## Download Project

### Clone

#### Using The Command Line

1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2
	```bash
	git clone https://github.com/FHPythonUtils/CheckPasswords
	```

More information can be found at
https://help.github.com/en/articles/cloning-a-repository

#### Using GitHub Desktop

1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files

### Licence

GPLv3 License (due to `pass-import` dependency)
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog

See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct

Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md)
 for more information.

### Contributing

Contributions are welcome, please see the
[Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md)
for more information.

### Security

Thank you for improving the security of the project, please see the
[Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md)
for more information.

### Support

Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
[Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md)
for more information.

### Rationale

The rationale acts as a guide to various processes regarding projects such as
the versioning scheme and the programming styles used. Please see the
[Rationale](https://github.com/FHPythonUtils/.github/blob/master/RATIONALE.md)
for more information.
