from pip._vendor.packaging.version import parse
import pkg_resources as pr
import platform
import urllib3
import json

try:
    from Packs.Utils.cliControl import listArgsCheck 
    from Packs.Utils.versionControl import lenfer
    from Packs.Utils.logger import Logger

except (ImportError, ModuleNotFoundError):
    from Utils.cliControl import listArgsCheck 
    from Utils.versionControl import lenfer
    from Utils.logger import Logger

class checker:
    def __init__(self, args, cli=False):
        if cli:
            self.run(args[2:])

        else:
            self.run(args)


    def __hasNumbers(self, t:str) -> bool:
        return any(i.isdigit() for i in t)


    def __validVersion(self, pyversion:str) -> bool:
        p = platform.python_version_tuple()[:2]
        p = lenfer("".join(p))

        pyversion = pyversion.replace('*', '0')

        validator = pyversion[:2]

        if self.__hasNumbers(validator):
            validator = validator[0]


        print(pyversion.replace(validator, '').split('.'))
        
        pyversion = lenfer("".join(pyversion.replace(validator, '').split('.')))

        return eval(f"{p} {validator} {pyversion}")

    def __drawVersion(self, version:str, key:str, p, requires:str) -> None:
        accept = ['py3', 'py2.py3', 'py3.py2', 'source', None]
        pyversion = True

        # if requires:
            # print(requires)
            # pyversion = self.__validVersion(requires)

        if version in accept and not p.is_devrelease and not p.is_postrelease and not p.is_prerelease and pyversion:
            print(f"{key:9}", end="")


    def __showVersions(self, pack:str, http) -> None:
        versions = http.request('GET', f"https://pypi.org/pypi/{pack}/json/")
        versions = json.loads(versions.data)
        Logger(f'{pack} versions available', 'yellow')

        c = 0
        
        for i in list(versions['releases'].keys()): 
            version = versions['releases'][i]
            
            if len(version) == 0:
                continue
            
            version = version[0]

            p = parse(i)

            self.__drawVersion(version['python_version'], i, p, version['requires_python'])

            if c == 8:
                print()
                c = -1

            c += 1


    def __local(self, pack:str, http) -> None:
        try:
            p = pr.get_distribution(pack)

        except pr.DistributionNotFound:
            Logger(f"Package {pack} not installed", 'red')
            return


        current = http.request("GET", f"https://pypi.org/pypi/{pack}/json/")
        current = json.loads(current.data)

        if current['info']['version'] == p.version:
            Logger(f"Package {pack} are installed on version {p.version}", 'green')

        else:
            Logger(f"Package {pack} are installed on version {p.version}, however there is a newer version of {pack}: {current['info']['version']}", 'yellow')


    def run(self, args:list) -> None:
        http = urllib3.PoolManager()
        commands = listArgsCheck(args)

        for i in commands[0]:
            if commands[1]:
                self.__local(i, http)

            else:
                self.__showVersions(i, http)
            Logger('\n')