from pip._vendor.packaging.version import parse
import datetime


def getVersions(lists:list, releases:list) -> dict:
    r = {}

    for i in lists:
        r[i] = releases[i]

    return r

def equals(version:str, releases:dict) -> list:
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
    versions = list(releases.keys())
    vs = version.replace(">", '').replace("=", '')

    try:
        num = versions.index(vs)

    except ValueError:
        vers = list(filter(lambda x: x.startswith(vs), versions))
        vers.sort()

        if len(vers) == 0:
            print(f'\033[91mVersion {vs} not found\033[37m')
            return {'msg': 'Error'}

        num = versions.index(vers[0])
        
        # versions.index(list(filter(lambda x: x.startswith(version), versions))[0])

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
    versions = list(releases.keys())
    vs = version.replace("<", '').replace("=", '')

    try:
        num = versions.index(vs)

    except ValueError:
        vers = list(filter(lambda x: x.startswith(vs), versions))
        vers.sort()

        if len(vers) == 0:
            print(f'\033[91mVersion {vs} not found\033[37m')
            return {'msg': 'Error'}

        num = versions.index(vers[0])

    if "=" in version:
        num += 1 

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
    
    more = moreThan(version, releases, bypass=True)

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
    l = []

    for i in lists[0]:
        lists[0][i].append(f'{i}')

        if len(lists) == 2 and i in lists[1]:
            l.append(lists[0][i])
        
        else:
            l.append(lists[0][i])
            
    return l


def combineDict(lists:list) -> dict:
    l = {}

    for i in lists[0]:
        if len(lists) == 2 and i in lists[1]:
            l[i] = lists[0][i]
        
        else:
            l[i] = lists[0][i]
            
    return l

def byteCalc(bytes:int) -> str:
    if bytes >= 100000:
        return f"{(bytes / 1000000):.2f} MB"

    return f"{bytes / 1000} KB"