from pip._vendor.packaging.version import parse
import datetime
import platform


def getVersions(lists:list, releases:dict) -> dict:
    """
    Transform list of versions and releases in dictionary of versions 

    Parameters
    ----------
    lists : list
        lisf of versions
    releases : dict
        dictionary of all releases in one package

    Returns
    -------
    dict
        dictionary of all releases belonging to the list of versions
    """

    r = {}

    for i in lists:
        r[i] = releases[i]

    return r

def equals(version:str, releases:dict) -> list:
    """
    Get a specific release 

    Parameters
    ----------
    version : str
        desired version
    releases : dict
        dictionary of all releases in one package

    Returns
    -------
    list
        desired release content
    """

    vx = version.replace("==", "").replace("(", '').replace(")", '').replace(" ", '')
    
    r = []
    try:
        remote = releases[f'{vx}']

        for i in remote:
            r.append(i)

        r.append(vx)
    
    except KeyError:
        return ["Error"]

    return r


def moreThan(version:str, releases:dict) -> dict:
    """
    Get releases thet are more than a specific version 

    Parameters
    ----------
    version : str
        desired version
    releases : dict
        dictionary of all releases in one package

    Returns
    -------
    list
        a releases that more than version specified
    """

    versions = list(releases.keys())
    vs = version.replace(">", '').replace("=", '')

    try:
        num = versions.index(vs)

    except ValueError:
        vers = list(filter(lambda x: x.startswith(vs), versions))
        vers.sort()

        if len(vers) == 0:
            num = len(versions) - 1
        
        else:
            num = versions.index(vers[0])

    if "=" not in version:
        num += 1 
    
    date = datetime.datetime.strptime(releases[versions[num]][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")
    rels = {}
    
    for i in releases:
        p = parse(i)

        if releases[i] == []:
            continue

        date2 = datetime.datetime.strptime(releases[i][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")

        if date2 >= date and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            rels[i] = releases[i]

    l = sorted(rels, key=lambda x: rels[x][0]['upload_time'])
    rels = getVersions(l, releases)

    return rels


def lessThan(version:str, releases:dict) -> dict:
    """
    Get releases thet are less than a specific version 

    Parameters
    ----------
    version : str
        desired version
    releases : dict
        dictionary of all releases in one package

    Returns
    -------
    list
        a releases that less than version specified
    """

    versions = list(releases.keys())
    vs = version.replace("<", '').replace("=", '')

    try:
        num = versions.index(vs)

    except ValueError:
        vers = list(filter(lambda x: x.startswith(vs), versions))
        vers.sort()

        if len(vers) == 0:
            num = len(versions) - 1

        else:
            num = versions.index(vers[0])

    if not "=" in version:
        num -= 1 

    date = datetime.datetime.strptime(releases[versions[num]][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")
    rels = {}
    
    for i in releases:
        p = parse(i)

        if releases[i] == []:
            continue

        date2 = datetime.datetime.strptime(releases[i][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")

        if date2 <= date and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            rels[i] = releases[i]

    l = sorted(rels, key=lambda x: rels[x][0]['upload_time'])
    rels = getVersions(l, releases)

    return rels


def equalSerie(version:str, releases:list) -> list:
    version = version.replace("~=", '').replace(")", '').replace("(", '')
    versions = list(releases.keys())
    
    more = moreThan(version, releases)

    try:
        versions.index(version)
        version = version.split(".")
        version.pop()

        version = ".".join(version)

    except ValueError:
        pass
    
    r = {}

    for i in releases:
        p = parse(i)

        if i.startswith(version) and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            r[i] = releases[i]
    
    l = sorted(r, key=lambda x: r[x][0]['upload_time'])
    r = getVersions(l, releases)

    c = combineDict([more, more])

    return c


def combine(lists:list) -> list:
    """
    Cross two lists where the values ​​are equal
 

    Parameters
    ----------
    lists : list
        list of lists

    Returns
    -------
    list
        a crossed list 
    """
    
    l = []

    for i in lists[0]:
        lists[0][i].append(f'{i}')

        if len(lists) == 2 and i in lists[1]:
            l.append(lists[0][i])
        
        else:
            l.append(lists[0][i])
            
    return l


def combineDict(lists:list) -> dict:
    """
    Cross two lists where the values ​​are equal
 

    Parameters
    ----------
    lists : list
        list of dictionary

    Returns
    -------
    list
        a crossed dictionary 
    """

    l = {}

    for i in lists[0]:
        if len(lists) == 2 and i in lists[1]:
            l[i] = lists[0][i]
        
        else:
            l[i] = lists[0][i]
            
    return l


def byteCalc(bytes:int) -> str:
    """
    Transform Bytes in MB or KB
 

    Parameters
    ----------
    bytes : int
        number of bytes

    Returns
    -------
    str
        a byte converted with yours measure 
    """
    
    if bytes >= 100000:
        return f"{(bytes / 1000000):.2f} MB"

    return f"{(bytes / 1000):.2f} KB"


def lenfer(txt:str) -> int:
    if len(txt) == 2:
        txt += "0"

    return int(txt)


def validVersionPython(version: str) -> bool:
    p = platform.python_version_tuple()[:2]
    p = lenfer("".join(p))

    version = version.split(" ")
    ev = version[0]
    version = lenfer(version[1].replace(".", ''))

    return eval(f"{p} {ev} {version}")