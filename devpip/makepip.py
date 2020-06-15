import subprocess
import platform
import sys
import os


class Makepip():
    def __init__(self, ar:list, commands:dict):
        self.__sysargs = ar
        self.__commands = commands

        if self.__sysargs[1].lower() == 'install' or self.__sysargs[1].lower() == 'i':
            self.__install()

        elif self.__sysargs[1].lower() == 'uninstall' or self.__sysargs[1].lower() == 'rm' or self.__sysargs[1].lower() == 'remove':
            self.__remove()

    
    def __install(self):
        procss = ['pip', 'install']

        for i in self.__sysargs[2:]:
            p = list(procss)
            p.append(i)

            print(f"\033[93mInstalling {i}\033[37m", end='\r')

            r = subprocess.run(p, stdout=subprocess.PIPE)

            if f'Requirement already satisfied: {i}' in r.stdout.decode():
                print(f"\033[92m{i} is already installed                         \n\033[37m")

            else:
                x = r.stdout.decode().split('Successfully installed ')[1].split(' ')[0].split('-')[1]
                print(f"\033[92m{i} installed in version {x}        \n\033[37m")

            try:
                r = r.stdout.decode().split("Successfully installed ")
                r = r[1].replace('\\r\\n', '').split(' ')

            except IndexError:
                continue

            print('Dependencies')

            for p in r:
                packageVersion = p.split('-')
                packageVersion = packageVersion[len(packageVersion) - 1]
            
                p = p.replace('-' + packageVersion, f'=={packageVersion}')
                
                if not p.lower().startswith(i.lower()):
                    print(p)
            
                with open('requirements.txt', 'a') as f:
                    f.write(p + '\r')


    def __remove(self):
        lines = []
        delPackages = []

        for i in self.__sysargs[2:]:
            while True:
                opt = input(f"\nDo you want remove {i} [y, n]\n>>> ")

                if opt.lower() == 'y' or opt.lower() == 'n':
                    if opt.lower() == 'y':
                        delPackages.append(i)
                        os.system(f'pip {commands[self.__sysargs[1].lower()]} {i} -y')
                    break
                
                else:
                    print('\n\033[91mType a valid option\033[37m\n')

        with open('requirements.txt', 'r') as f:
            lines = f.readlines()

        with open('requirements.txt', 'w') as f:
            for i in lines:
                b = True

                for j in delPackages:
                    if i.lower().split('==')[0] == j or i == '\r' or i == '\n':
                        b = False
                        break
                    
                if b:
                    f.write(i)


if __name__ == '__main__':
    if hasattr(sys, 'real_prefix'):
        commands = {
            'install': 'install', 
            'i': 'install', 
            'uninstall': 'uninstall', 
            'remove': 'uninstall', 
            'rm': 'uninstall'
        }

        if len(sys.argv) <= 2:
            print("\nChoose an option and package\n")

            print('\033[92m install   <package>\033[37m  to install a package')
            print('\033[92m i         <package>\033[37m  to install a package\n')
            print('\033[92m uninstall <package>\033[37m  to uninstall a package')
            print('\033[92m remove    <package>\033[37m  to uninstall a package')
            print('\033[92m rm        <package>\033[37m  to uninstall a package\n')

        elif sys.argv[1].lower() not in commands:
            print('\033[91m Invalid command\033[37m')

        else:
            Makepip(sys.argv, commands)

    else:
        print("Please activate the virtual environment to use DevPip")