<p align="center">
    <img src="https://raw.githubusercontent.com/Vupy/Packs/master/Packs/logo/logo.png" width="256" height="256"/>
</p>

[![Documentation Status](https://readthedocs.org/projects/packs/badge/?version=latest)](https://packs.readthedocs.io/en/latest/?badge=latest)

# Packs

Packs is a package installer that will help you manage your dependencies in a practical way.

for that, packs automatically manage their packages including them in the dependency files (requirements.txt and requirements-dev.txt). The packs in addition to managing it also provides you to separate them into development and production packages.

## Installation

> Packs requires python version >= 3.5 and Urllib3

```
pip install packs
```

## Usage

Before starting any installation or removal of packages through the Packs, two files will be generated:

* requirements.txt 
> Production dependency
* requirements-dev.txt 
> Development dependency

As you add or remove dependencies for a project through the Packs, it will add or remove the dependencies you changed. Example

packs i pillow -d

After running the command above, the Packs will add the Pillow package to the requirements-dev.txt (-d) file with its respective version of Pillow.

**Note** that the Packs does not distinguish between upper and lower case, that is, commands can be written in any format.

* packs insTall Pillow  -> OK
* packs Install Pillow  -> OK
* packs InStAlL Pillow  -> OK


To install any package, you can use the following commands and flags:

```
packs install <Package name>
packs i <Package name>

-u To update
-d or --dev To development packages
-r <file path> to install the packages through a file
```

To remove any package use the following commands and flags:

```
packs remove <Package name>
packs uninstall <Package name>
packs rm <Package name>

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

To see the list of package versions available on / offline use this commands and flags:

```
packs check <Package name>

--local or -l to see if the package is installed locally and is up to date
```

To manipulate the saved cache use this command and the flags:

```
packs cache
-c to clear cache
-l to list packages in cache
```

<strong>
    <p align="center" style="text-align: center;">Vupy social networking 2020</p>
</strong>