from pip._vendor.packaging.version import parse
import datetime


def getVersions(lists:list, releases:list) -> dict:
    r = {}

    for i in lists:
        r[i] = releases[i]

    return r

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
    
    date = datetime.datetime.strptime(releases[versions[num]][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")
    
    rels = {}
    
    for i in releases:
        p = parse(i)
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
        print(f'\033[91mVersion {vs} not found\033[37m')
        return {'msg': 'Error'}

    if "=" in version:
        num += 1 

    date = datetime.datetime.strptime(releases[versions[num]][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")
    
    rels = {}
    
    for i in releases:
        p = parse(i)
        date2 = datetime.datetime.strptime(releases[i][0]['upload_time'], "%Y-%m-%dT%H:%M:%S")

        if date2 <= date and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease:
            rels[i] = releases[i]

    l = sorted(rels, key=lambda x: rels[x][0]['upload_time'])
    rels = getVersions(l, releases)

    return rels


def equalSerie(version:str, releases:list) -> list:
    pass


def combine(lists:list) -> list:
    l = []

    for i in lists[0]:
        lists[0][i].append(f'{i}')

        if len(lists) == 2 and i in lists[1]:
            l.append(lists[0][i])
        
        else:
            l.append(lists[0][i])
            
    return l