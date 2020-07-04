import os


def openToCreate() -> None:
    if not os.path.exists('requirements.txt'):
        f = open("requirements.txt", "w")
        f.close()

    if not os.path.exists('requirements-dev.txt'):
        f = open("requirements-dev.txt", "w")
        f.close()



def addDependencies(dependency:str, dev:bool = False) -> None:
    """
    Add new dependencies to dependencies file (requirements)

    Parameters
    ----------
        dependency : str
            name of dependency that will be added
        dev : bool
            if this dependency is a dev dependency

    >>> addDependencies('package==1.2.3', True)
    None

    >>> addDependencies('package==1.2.3', False)
    None
    """
    
    fil = 'requirements-dev.txt' if dev else 'requirements.txt'
    lines = []

    with open(fil, 'r') as f:
        lines = [i.replace('\n', '').lower() for i in f.readlines() if i != '\n']

    with open(fil, 'a') as f:
        b = True
        for i in lines:
            if i.split("==")[0].lower() == dependency.split('==')[0].lower():
                b = False
                break

        if b and dependency not in lines:
            f.write(f"{dependency}\n")


def notInList(filer:str, dependency:str) -> None:
    lines = []
    try:
        with open(filer, 'r') as f:
            lines = f.readlines()

    except Exception as e:
        print(e)
        return

    with open(filer, 'w') as f:
        for i in lines:
            if i.lower().replace('\n', '').replace('\r', '') == dependency.lower():
                continue

            f.write(i)
    

def removeDependency(dependency:str) -> None:
    notInList('requirements.txt', dependency)
    notInList('requirements-dev.txt', dependency)
