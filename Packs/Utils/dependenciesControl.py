def openToCreate() -> None:
    f = open("requirements.txt", "w")
    f.close()

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
    
