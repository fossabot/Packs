from typing import Generator
import subprocess
import platform
import sys
import os


class Main():
    def __init__(self, ar:list) -> None:
        self.__sysargs = ar
        
        if __name__ == '__main__':
            if self.__sysargs[1].lower() == 'install' or self.__sysargs[1].lower() == 'i':
                print(list(self.install()))

            elif self.__sysargs[1].lower() == 'uninstall' or self.__sysargs[1].lower() == 'rm' or self.__sysargs[1].lower() == 'remove':
                list(self.remove())


    def __readLinesFile(self, fileReq:str, delPackages:list) -> None:
        with open(fileReq, 'r') as f:
            lines = f.readlines()

        with open(fileReq, 'w') as f:
            for i in lines:
                b = True

                for j in delPackages:
                    if i.lower().split('==')[0] == j or i == '\r' or i == '\n' or i == '\r\n':
                        b = False
                        break
                    
                if b:
                    f.write(i)


    def install(self):
        procss = ['pip', 'install']

        generalCommands = ['--dev', '-d', '-u']

        dev = (lambda x: '--dev' in x or '-d' in x)(self.__sysargs[2:])
        upd = (lambda x: '-u' in x)(self.__sysargs[2:])

        if upd:
            procss.append('-U')

        for i in self.__sysargs[2:]:
            p = list(procss)

            if i in generalCommands:
                continue

            p.append(i)

            print(f"\033[93mInstalling {i}\033[37m", end='\r')

            r = subprocess.run(p, stdout=subprocess.PIPE)

            if r.returncode == 1:
                print(f"\n\033[37m")
                yield 'error'
                continue

            if f'Requirement already satisfied: {i}' in r.stdout.decode():
                print(f"\033[92m{i} is already installed                         \n\033[37m")
                yield 'ok'

            else:
                x = r.stdout.decode().split('Successfully installed ')[1].split(' ')[0].split('-')[1]
                print(f"\033[92m{i} installed in version {x}        \n\033[37m")
                yield 'ok'

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
            
                with open('requirements-dev.txt' if dev else 'requirements.txt', 'a') as f:
                    f.write(p + '\r')

            
    def remove(self):
        delPackages = []
        generalCommands = ['--yes', '-y']

        yes = (lambda x: '--yes' in x or '-y' in x)(self.__sysargs[2:])

        for i in self.__sysargs[2:]:
            if i in generalCommands:
                continue
            while True:

                if yes:
                    opt = 'y'

                else:
                    opt = input(f"\nDo you want remove {i} [y, n]\n>>> ")

                if opt.lower() == 'y' or opt.lower() == 'n':
                    if opt.lower() == 'y':
                        delPackages.append(i)
                        os.system(f'pip {commands[self.__sysargs[1].lower()]} {i} -y')
                    
                    yield 'valid'
                    break
                
                else:
                    print('\n\033[91mType a valid option\033[37m\n')
                    yield 'invalid'

        self.__readLinesFile('requirements.txt', delPackages)
        self.__readLinesFile('requirements-dev.txt', delPackages)


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
            print('\033[92m i         <package>\033[37m  to install a package')
            print('\033[92m --dev              \033[37m  to install development packages')
            print('\033[92m -d                 \033[37m  to install development packages')
            print('\033[92m -u                 \033[37m  to update a package\n')
            
            print('\033[92m uninstall <package>\033[37m  to uninstall a package')
            print('\033[92m remove    <package>\033[37m  to uninstall a package')
            print('\033[92m rm        <package>\033[37m  to uninstall a package')
            print('\033[92m --yes              \033[37m  to accept all\n')
            print('\033[92m -y                 \033[37m  to accept all\n')

        elif sys.argv[1].lower() not in commands:
            print('\033[91m Invalid command\033[37m')

        else:
            Main(sys.argv)

    else:
        print("Please activate the virtual environment to use DevPip")