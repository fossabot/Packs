def pureDependency(dependency:str) -> str:
    """
    Get the name of package 

    Parameters
    ----------
    dependency : str
        package

    Returns
    -------
    str
        a name of package without the version

    >>> pureDependency('package==1.2.3')
    'package'
    """

    dependency = dependency.split("==")[0]
    dependency = dependency.split(">")[0]
    dependency = dependency.split("<")[0]
    dependency = dependency.split("~=")[0]
    dependency = dependency.split("=")[0]
    
    return dependency


def checkfiles(fileR:str, comp:list) -> list:
    """
    Open a specific file that provided by the user in the CLI 

    Parameters
    ----------
    fileR : str
        name of file
    comp : list
        command list

    Returns
    -------
    list
        a list of commands with the contents of the file
    """

    try:
        with open(fileR, 'r') as f:
            for j in f.readlines():
                b = True

                for i in comp:
                    if pureDependency(i) == pureDependency(j):
                        b = False
                        break

                if b:
                    j = j.replace('\n', '').replace('\r', '')
                    comp.append(j)

    except FileNotFoundError:
        print(f'\033[91mERROR file {fileR} not found\033[37m')

    return comp


def fileAarg(commands:list) -> list:
    """
    Finds file parameters within a CLI list 

    Parameters
    ----------
    commands : list
        command list

    Returns
    -------
    list
        a list of the packages that will be installed
    """

    is_file = False
    c = commands

    for i in commands:
        if i == '-r':
            is_file = True
            continue

        if is_file:
            is_file = False
            c.remove(i)
            c = checkfiles(i, c)
            
    return c


def listArgsInstall(commands:list) -> list:
    """
    Get the CLI and apply the necessary changes by the args flag

    Parameters
    ----------
    commands : list
        command list

    Returns
    -------
    list
        a filtered list of the packages that will be installed

    >>> listArgsInstall(['pack1', 'pack2', '-d', '-r', 'file.txt'])
    [['pack1', 'pack2', 'filePack1', 'filePack2'], True, False]
    """

    d = False
    u = False
    args = ['-d', '--dev', '-u', '-r']

    commands = [i.lower() for i in commands]

    if '-d' in commands or '--dev' in commands:
        d = True

    if '-u' in commands:
        u = True

    if '-r' in commands:
        commands = fileAarg(commands)
    
    commands = [i for i in commands if i not in args]

    return [commands, d, u]


def listArgsRemove(commands:list) -> list:
    y = False
    args = ['-y', '--yes', '-r']

    commands = [i.lower() for i in commands]

    if '-y' in commands or '--yes' in commands:
        y = True

    if '-r' in commands:
        commands = fileAarg(commands)

    commands = [i for i in commands if i not in args]

    return [commands, y]


def listArgsList(commands:list) -> list:
    c = False
    f = False
    args = ['-c', '-f', '--color', '--freeze']

    commands = [i.lower() for i in commands]

    if '-f' in commands or '--freeze' in commands:
        f = True

    if '-c' in commands or '--color' in commands:
        c = True

    commands = [i for i in commands if i not in args]

    return [commands, f, c]


def listArgsCheck(commands:list) -> list:
    l = False

    args = ['-l', '--local']

    commands = [i.lower() for i in commands]

    if '-l' in commands or '--local' in commands:
        l = True

    commands = [i for i in commands if i not in args]
    
    return [commands, l]