from pip._vendor.packaging.version import parse


def equals(version:str, releases:list) -> list:
    vx = version.replace("==", "").replace("(", '').replace(")", '')
    
    try:
        remote = [i for i in releases[f'{vx}'] if i['url'].endswith('.whl')]
    
    except KeyError:
        return ["Error"]

    return remote


def moreThan(version:str, releases:dict) -> dict:
    versions = list(releases.keys())
    vs = version.replace(">", '').replace("=", '')
    try:
        num = versions.index(vs)

    except ValueError:
        print(f'\033[91mVersion {vs} not found\033[37m')
        return {'msg': 'Error'}

    if "=" not in version:
        num += 1 

    versions = versions[num:]
    
    rels = {}
    
    for i in releases:
        p = parse(i)
        if i in versions and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            rels[i] = releases[i]

    return rels


def lessThan(version:str, releases:list) -> list:
    versions = list(releases.keys())
    vs = version.replace("<", '').replace("=", '')

    try:
        num = versions.index(vs)

    except ValueError:
        print(f'\033[91mVersion {vs} not found\033[37m')
        return {'msg': 'Error'}

    if "=" in version:
        num += 1 

    versions = versions[:num]
    
    rels = {}
    
    for i in releases:
        p = parse(i)

        if i in versions and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            rels[i] = releases[i]

    return rels


def equalSerie(version:str, releases:list) -> list:
    pass


def combine(lists:list) -> list:
    if len(lists) == 1:
        return lists[0]

    l = []
    for i in lists[0]:
        if i in lists[1]:
            lists[0][i].append(f'{i}')
            l.append(lists[0][i])
            
    return l