import sys
import os

try:
    import Packs.checkRequirements
    from Packs.Commands import install, remove, listPackage, check

except (ModuleNotFoundError, ImportError):
    import checkRequirements
    from Commands import install, remove, listPackage, check


def main():
    if hasattr(sys, 'real_prefix'):
       
        commands = {
            'install': install.Installer, 
            'i': install.Installer, 
            'uninstall': remove.Remover, 
            'remove': remove.Remover, 
            'rm': remove.Remover,
            'ls': listPackage.Lister,
            'list': listPackage.Lister,
            'check': check.checker,
        }

        dropping = ['ls', 'list']

        if len(sys.argv) == 1 or (len(sys.argv) <= 2 and sys.argv[1] not in dropping):
            print("\nChoose an option and package\n")

            print('\033[92m install         <packages>\033[37m  to install a package')
            print('\033[92m i               <packages>\033[37m  to install a package')
            print('\033[92m -r              <filePath>\033[37m  to list of packages in file')
            print('\033[92m --dev or -d               \033[37m  to install development packages')
            print('\033[92m -u                        \033[37m  to update a package\n')
            
            print('\033[92m uninstall       <packages>\033[37m  to uninstall a package')
            print('\033[92m remove          <packages>\033[37m  to uninstall a package')
            print('\033[92m rm              <packages>\033[37m  to uninstall a package')
            print('\033[92m -r              <filePath>\033[37m  to list of packages in file')
            print('\033[92m --yes or -y               \033[37m  to accept all\n')

            print('\033[92m list                      \033[37m  to list all packages')
            print('\033[92m ls                        \033[37m  to list all packages')
            print('\033[92m -f or --freeze            \033[37m  to list all packages in freeze format\n')

            print('\033[92m check           <packages>\033[37m  to list all version of a package list')
            print('\033[92m -l or --local             \033[37m  to list all version of a package list that are installed\n')

        elif sys.argv[1].lower() not in commands:
            print('\033[91mInvalid command\033[37m')

        else:
            commands[sys.argv[1].lower()](sys.argv, cli=True)

    else:
        print("\n\033[91mPlease activate the virtual environment to use Packs\n\033[37m")



if __name__ == '__main__':
    main()