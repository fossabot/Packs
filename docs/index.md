# Packs

Packs is a package installer that will help you manage your dependencies in a practical way.

for that, packs automatically manage their packages including them in the dependency files (requirements.txt and requirements-dev.txt). The packs in addition to managing it also provides you to separate them into development and production packages.

## Installation

´´´
pip install packs
´´´

## Usage

To install any package, you can use the following commands and flags:

```
python main.py install <Package name>
python main.py i <Package name>

-u To update
--dev or -d To development packages
-r <file path> to install the packages through a file
```

To remove any package use the following commands and flags:

```
python main.py remove <Package name>
python main.py uninstall <Package name>
python main.py rm <Package name>

--yes or -y to accept all
-r <file path> to remove the packages through a file
```

To list the installed packages use this commands and flags:

```
packs ls
packs list

--freeze or -f to list in freeze format
--color or -c to remove the colors
```

<strong>
    <p align="center" style="text-align: center;">Vupy social networking 2020</p>
</strong>
