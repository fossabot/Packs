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
                list(self.install())

            elif self.__sysargs[1].lower() == 'uninstall' or self.__sysargs[1].lower() == 'rm' or self.__sysargs[1].lower() == 'remove':
                list(self.remove())


    def __readLinesFile(self, fileReq:str, delPackages:list) -> None:
        try:
            with open(fileReq, 'r') as f:
                lines = f.readlines()

        except FileNotFoundError:
            return

        with open(fileReq, 'w') as f:
            for i in lines:
                b = True

                for j in delPackages:
                    if i.lower().split('==')[0] == j or i == '\r' or i == '\n' or i == '\r\n':
                        b = False
                        break
                    
                if b:
                    f.write(i)


    def __normalizePacks(self, fileReq:str, packs:dict) -> None:
        try:
            with open(fileReq, 'r') as f:
                lines = f.readlines()

        except FileNotFoundError:
            return

        with open(fileReq, 'w') as f:
            for i in lines:
                b = True
                for j in packs:
                    if i.lower().split("==")[0] == j and i.lower().replace('\n', '').replace('\r', '') != packs[j].replace('\n', '').replace('\r', ''):
                        b = False
                        break
                    
                if b and i != '\n':
                    f.write(i)


    def __flatPacks(self, fileReq:str) -> None:
        try:
            with open(fileReq, 'r') as f:
                lines = f.readlines()

        except FileNotFoundError:
            return

        with open(fileReq, 'w') as f:
            for i in lines:                   
                if i != '\n':
                    f.write(i)


    def __installProcess(self, packIns:str, command:list, filereq:str):
        packs = {}
        print(f"\033[93mInstalling {packIns}\033[37m", end='\r')

        r = subprocess.run(command, stdout=subprocess.PIPE)

        if r.returncode == 1:
            print(f"\n\033[37m")
            return 'error'

        if f'Requirement already up-to-date: {packIns}' in r.stdout.decode():
            print(f"\033[92m{packIns} is already installed                         \n\033[37m")
            return 'okc'

        if f'Requirement already satisfied: {packIns}' in r.stdout.decode():
            print(f"\033[92m{packIns} is already installed                         \n\033[37m")

        else:
            x = r.stdout.decode().split('Successfully installed ')[1].split(' ')[0].split('-')[1]
            print(f"\033[92m{packIns} installed in version {x}        \n\033[37m")

        try:
            r = r.stdout.decode().split("Successfully installed ")
            r = r[1].replace('\\r\\n', '').split(' ')

        except IndexError:
            return 'okc'

        if len(r) > 1:
            print('Dependencies')


        for p in r:
            packageVersion = p.split('-')
            packageVersion = packageVersion[len(packageVersion) - 1]
        
            p = p.replace('-' + packageVersion, f'=={packageVersion}')
            
            if not p.lower().startswith(packIns.lower()):
                print(p)

            # if upd:
            packs[f"{p.split('==')[0].lower()}"] = p
        
            with open(filereq, 'a') as f:
                f.write(p + '\r')
        
        return packs


    def install(self):
        procss = ['pip', 'install']

        generalCommands = ['--dev', '-d', '-u', '-r']

        dev = (lambda x: '--dev' in x or '-d' in x)(self.__sysargs[2:])
        upd = (lambda x: '-u' in x)(self.__sysargs[2:])

        packs = {}
        isFile = False
        
        if upd:
            procss.append('-U')

        for i in self.__sysargs[2:]:
            p = list(procss)

            if i.lower() in generalCommands:
                if i.lower() == '-r':
                    isFile = True

                continue

            if isFile:
                try:
                    with open(i, 'r') as f:
                        lines = f.readlines()
                        # como = list(p)

                        for i in lines:
                            p.append(i.replace('\n', '').replace('\r', ''))
                            res = self.__installProcess(
                                i.replace('\n', '').replace('\r', ''), 
                                p, 
                                'requirements-dev.txt' if dev else 'requirements.txt'
                            )

                            if res == 'error' or res == 'okc':
                                if res == 'okc':
                                    yield 'ok'

                                else:
                                    yield 'error'

                                continue

                            yield 'ok'
                            
                            packs = {
                                **packs,
                                **res
                            }

                            p.pop()

                except FileNotFoundError:
                    print(f"\033[91mFile {i} not founded\033[37m")
                
                isFile = False

            else:
                p.append(i)

                res = self.__installProcess(i, p, 'requirements-dev.txt' if dev else 'requirements.txt')

                if res == 'error' or res == 'okc':
                    if res == 'okc':
                        yield 'ok'

                    else:
                        yield 'error'

                    continue

                yield 'ok'
                
                packs = {
                    **packs,
                    **res
                }

        if upd:
            self.__normalizePacks('requirements-dev.txt', packs)
            self.__normalizePacks('requirements.txt', packs)

        else:
            self.__flatPacks('requirements-dev.txt')
            self.__flatPacks('requirements.txt')

            
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
            print('\033[92m -r       <filePath>\033[37m  to list of packages')
            print('\033[92m --dev or -d        \033[37m  to install development packages')
            print('\033[92m -u                 \033[37m  to update a package\n')
            
            print('\033[92m uninstall <package>\033[37m  to uninstall a package')
            print('\033[92m remove    <package>\033[37m  to uninstall a package')
            print('\033[92m rm        <package>\033[37m  to uninstall a package')
            print('\033[92m --yes or -y        \033[37m  to accept all\n')

        elif sys.argv[1].lower() not in commands:
            print('\033[91m Invalid command\033[37m')

        else:
            Main(sys.argv)

    else:
        print("Please activate the virtual environment to use DevPip")