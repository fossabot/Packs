import subprocess
import platform
import sys
import os


def makepip():
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
            
            return False

        elif sys.argv[1].lower() not in commands:
            print('\033[91m Invalid command\033[37m')
            return False

        if sys.argv[1].lower() == 'install' or sys.argv[1].lower() == 'i':
            r = subprocess.run(['pip', commands[sys.argv[1].lower()], *sys.argv[2:]], stdout=subprocess.PIPE)

            print(r.stdout.decode())

            r = r.stdout.decode().split("Successfully installed ")
            r = r[1].replace('\\r\\n', '').split(' ')

            for i in r:
                packageVersion = i.split('-')
                packageVersion = packageVersion[len(packageVersion) - 1]
            
                i = i.replace('-' + packageVersion, f'=={packageVersion}')
                print(i)
            
                with open('requirements.txt', 'a') as f:
                    f.write(i + '\r')

        else:
            lines = []
            delPackages = []

            for i in sys.argv[2:]:
                while True:
                    opt = input(f"Do you want remove {i} [y,n]\n>>> ")

                    if opt.lower() == 'y' or opt.lower() == 'n':
                        if opt.lower() == 'y':
                            delPackages.append(i)
                            os.system(f'pip {commands[sys.argv[1].lower()]} {i} -y')
                        break
                    
                    else:
                        print('\n\033[91mType a option\033[37m\n')

            with open('requirements.txt', 'r') as f:
                lines = f.readlines()

            with open('requirements.txt', 'w') as f:
                for i in lines:
                    b = True

                    for j in delPackages:
                        if i.lower().split('==')[0] == j:
                            b = False
                            break

                    if b:
                        f.write(i)
    else:
        print("Please activate the virtual environment to use DevPip")


if __name__ == '__main__':
    # r = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    # print(r.stdout)
    makepip()