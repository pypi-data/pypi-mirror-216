```
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████
████████████████    ███████████████                                  ███              ███                      ██
███████████████████████████████████                                 ░░░      ██████  ░░░                       ██
██          ██      ████        ███  █████ █████  ██████  ████████  ████    ███░░███ ████   ██████  ████████   ██
███    ██    ███    ███    ██    ██  ░███ ░░███  ███░░███░░███░░███░░███   ░███ ░░░ ░░███  ███░░███░░███░░███  ██
███    ██    ███    ███    ██    ██  ░███  ░███ ░███████  ░███ ░░░  ░███  ███████    ░███ ░███████  ░███ ░░░   ██
███    ██    ███    ███    ██    ██  ░░███ ███  ░███░░░   ░███      ░███ ░░░███░     ░███ ░███░░░   ░███       ██
███         ██        ██        ███   ░░█████   ░░██████  █████     █████  ░███      █████░░██████  █████      ██
███    ████████████████████████████    ░░░░░     ░░░░░░  ░░░░░     ░░░░░   ░███     ░░░░░  ░░░░░░  ░░░░░       ██
███    ████████████████████████████                                        ░███                                ██
███    ██████████████████████████████████████████████████████████████████████████████████████████████████████████
```
[![PyPI-Version][version-badge]][version-link] [![PyPI-License][license-badge]](LICENSE)


**Pioverifier** is a simple CLI tool that allows you to verify *platformio.ini* config file
for [PlatformIO](https://platformio.org "Professional collaborative platform for embedded development")-based projects.
It is distributed as a Python package on [PyPI](https://pypi.org "Python Package Index").

## **Package is currently on *planning* stage**
**All the paragraphs below do not reflect the actual functionality for now.**

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started "pip documentation"):
``` batchfile
pip install --upgrade pioverifier
```

## Usage

Considering your project has the following structure:
```
project-dir
├── ... (project dirs and files)
└── platformio.ini
```

run these commands in a terminal to perform a verification:
``` batchfile
cd path\to\project-dir
python -m pioverifier
```

alternatively, you can run an equivalent one-line command:
``` batchfile
python -m pioverifier --project-path="path\to\project-dir"
```

[version-badge]: https://img.shields.io/pypi/v/pioverifier?style=flat-square
[version-link]:  https://pypi.python.org/pypi/pioverifier
[license-badge]: https://img.shields.io/pypi/l/pioverifier?style=flat-square
