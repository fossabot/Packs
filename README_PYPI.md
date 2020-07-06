# Packs

Packs is a package that assists Pip in installing and managing packages. With Pip it is possible to install several packages for Python, however when generating the requirements.txt file there will always be some packages that are not needed for the production environment. And in this context, the Packs can assist you with development and production packages.

When installing any package it is possible to add the flag --dev or just -d so that it is defined that this package will only be for the development environment and not for production. At the end of any installation or removal of packages, the Packs will automatically generate two files: requirements.txt and requirements-dev.txt, which represent the production and development dependency list respectively.

## Installation

pip install packs

## Usage 

To install any package, you can use the following commands and flags:

```
packs install <Package name>
packs i <Package name>

-u To update
--dev or -d To development packages
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


<strong>
    <p align="center" style="text-align: center;">Vupy social networking 2020</p>
</strong>