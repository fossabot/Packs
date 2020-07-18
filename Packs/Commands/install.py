from wheel.pep425tags import get_abi_tag
from typing import Callable
import pkg_resources as pr
from time import sleep
import subprocess
import itertools
import tempfile
import platform
import tarfile
import urllib3
import shutil
import json
import sys
import os

try:
    from pip._internal.operations.install.wheel import install_wheel
    from pip._internal.locations import get_scheme
    import wheel

except ModuleNotFoundError:
    print("\033[91m\nPlease activate the virtual environment to use Packs\n\033[37m")
    sys.exit(0)

try:
    from Packs.Utils.versionControl import (lessThan, moreThan, equals, byteCalc, combine, equalSerie, validVersionPython)
    from Packs.Utils.dependenciesControl import addDependencies, openToCreate, removeDependency
    from Packs.Utils.cliControl import listArgsInstall, pureDependency
    from Packs.Utils.logger import Logger
    from Packs.Commands import remove

except (ModuleNotFoundError, ImportError):
    from Utils.versionControl import (lessThan, moreThan, equals, byteCalc, combine, equalSerie, validVersionPython)
    from Utils.dependenciesControl import addDependencies, openToCreate, removeDependency
    from Utils.cliControl import listArgsInstall, pureDependency
    from Utils.logger import Logger
    from Commands import remove


class Installer:
    def __init__(self, args:list, cli=False):
        temp = tempfile.gettempdir()
        self.__deps = []
        self.__dev = False
        self.__u = False
        
        openToCreate()

        if not os.path.exists(temp + "/packsX"):
            os.mkdir(temp + "/packsX")

        if (cli):
            self.run(args[2:])
            
        else:
            self.run(args)


    def __normalizeVersion(self, version:str, res:list) -> list:
        version = version.lower().replace(res['info']['name'].lower(), '')
        releases = res['releases']

        versionControl = {
            "<": lessThan,
            "==": equals,
            '~': equalSerie,
            '>': moreThan,
        }

        if "=" in version or ">" in version or "<" in version or "~=" in version:
            if "==" in version:
                return versionControl['=='](version, releases)

            else:
                vx = version.replace("(", '').replace(")", '').replace(' ', '').split(',')
                l = []

                for i in vx:
                    track = versionControl[i[0]](i, releases)

                    if "msg" in track:
                        return 'ErrorV'

                    l.append(track)

                c = combine(l)

                if len(c) > 0:
                    return c[len(c) - 1]

                return "ErrorR"

        c = releases[res['info']['version']]
        c.append(res['info']['version'])
        
        return c


    def __wheelInstall(self, name:str, filewhl:str) -> bool:
        try:
            pack = pr.get_distribution(name)

        except Exception:
            scheme = get_scheme(
                name,
                user=False,
                home=None,
                root=None,
                prefix=None,
            )

            install_wheel(
                name,
                filewhl,
                scheme=scheme,
                req_description=name,
                pycompile=True,
            )

            return False

        if self.__u:
            removeDependency(f"{pack.key}=={pack.version}")

            scheme = get_scheme(
                name,
                user=False,
                home=None,
                root=None,
                prefix=None,
            )

            install_wheel(
                name,
                filewhl,
                scheme=scheme,
                req_description=name,
                pycompile=True,
            )

            return False

        return True


    def __tarInstall(self, name:str, filewhl:str) -> bool:
        temp = tempfile.gettempdir()
        p = os.getcwd()

        try:
            pack = pr.get_distribution(name)

        except Exception:
            with tarfile.open(filewhl, 'r:gz') as tar:
                tar.extractall(temp + "/packsX")

            os.chdir(filewhl.replace(".tar.gz", ''))

            FNULL = open(os.devnull, 'w')

            subprocess.run(['python', 'setup.py', 'install'], stdout=FNULL, stderr=subprocess.PIPE)

            os.chdir(p)
            return False

        if self.__u:
            removeDependency(f"{pack.key}=={pack.version}")

            with tarfile.open(filewhl, 'r:gz') as tar:
                tar.extractall(temp + "/packsX")

            os.chdir(filewhl.replace(".tar.gz", ''))

            FNULL = open(os.devnull, 'w')

            subprocess.run(['python', 'setup.py', 'install'], stdout=FNULL, stderr=subprocess.PIPE)
            
            os.chdir(p)

            return False

        return True


    def __cpythonChecker(self, vers:list) -> list:
        vs = []

        for i in vers:
            if i['python_version'] == get_abi_tag():
                vs.append(i)

        if len(vs) == 0:
            return vers[0]

        return vs


    def __archAndSystemChecker(self, vers:list, typex:str, arc:str) -> list:
        vs = []

        for i in vers:
            if typex in i['filename'] and arc in i['filename']:
                vs.append(i)

        return vs


    def  __processerChecker(self, vers:list) -> list:
        system = platform.system()

        if system == "Windows":
            typex = "-win32"
            arc = ""

        elif system == "Linux":
            typex = "-manylinux"
            arc = platform.machine()

        else:
            typex = "-macosx_"
            arc = platform.machine()

        return self.__archAndSystemChecker(vers, typex, arc)


    def __checkTypeInstallation(self, vers:list) -> list:
        remote = [i for i in vers if i['url'].endswith('.whl')]

        if len(remote) == 0:
            return [vers[0], self.__tarInstall]

        elif len(remote) == 1:
            return [remote[0], self.__wheelInstall]

        else:
            
            return [self.__cpythonChecker(self.__processerChecker(vers))[0], self.__wheelInstall]


    
    def __downloadPackage(self, url:str, filew:str, http) -> None:
        if os.path.exists(filew):
            return

        files = http.request("GET", url)

        with open(filew, "wb") as f:
            f.write(files.data)

    
    def __installPackageDependencies(self, res:dict, http, version:str) -> list:
        temp = tempfile.gettempdir()

        vers = self.__normalizeVersion(version, res)
        vx = vers.pop()

        if vers == "ErrorR":
            Logger("ERROR there is no version that satisfies the condition", 'red')
            return

        if vers == "ErrorV":
            return
        
        remote = self.__checkTypeInstallation(vers)

        self.__downloadPackage(remote[0]['url'], temp + f"/packsX/{remote[0]['filename']}", http)
        return [remote[1](res['info']['name'], temp + f"/packsX/{remote[0]['filename']}"), remote[0]['size'], vx]
        

    def __installPackage(self, res:dict, http, version:str) -> str:
        temp = tempfile.gettempdir()
        vers = self.__normalizeVersion(version, res)
        v = vers.pop()

        if vers == "ErrorR":
            Logger("ERROR there is no version that satisfies the condition", 'red')
            return

        if vers == "ErrorV":
            return "error"
        
        remote = self.__checkTypeInstallation(vers)

        Logger(f"\nPackage {res['info']['name']} found in version {v} ({byteCalc(remote[0]['size'])})", 'green')

        ### DOWNLOAD

        Logger(f"\nDownloading {res['info']['name']}", 'pink', end='\r')
        self.__downloadPackage(remote[0]['url'], temp + f"/packsX/{remote[0]['filename']}", http)
        Logger(f"{'Download finish':50}", 'green')

        ### INSTALL 

        Logger(f"\nInstalling {res['info']['name']}", 'pink', end='\r')
        whl = remote[1](res['info']['name'], temp + f"/packsX/{remote[0]['filename']}")
        
        if not whl:
            addDependencies(f"{res['info']['name']}=={v}", self.__dev)
            Logger(f"{res['info']['name']} was successfully installed", 'green')

        else:
            Logger(f"{res['info']['name']} already installled", 'blue')

        return remote[0]


    def __dependenciesLoop(self, reqs:list, fun:Callable, http, spacer:int = 3):
        for i in reqs:
            if '; extra' in i or i.split(' ')[0] in self.__deps or "and extra" in i: 
                continue
            
            if "; python_version" in i and not validVersionPython(i.split("; python_version ")[1].replace('"', '')):
                continue

            i = i.split(" ; ")[0]
            self.__deps.append(i.split(' ')[0])

            Logger(f"{' ' * spacer}{i.split(' ')[0]}", end="\r")
            
            a = fun(i, http, spacer)
            
            Logger(f"{' ' * spacer}{a[0]}", 'green')

            if len(a) > 1:
                a[1](*a[2])

    
    def __dependencies(self, pack:str, http, spacer:int) -> list:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack.split(' ')[0]}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())
        inst = self.__installPackageDependencies(packinfo, http, pack)

        ret = [f"{packinfo['info']['name']}=={inst[2]} ({byteCalc(inst[1])})"]

        if packinfo['info']['requires_dist']:
            ret.append(self.__dependenciesLoop)
            ret.append([packinfo['info']['requires_dist'], self.__dependencies, http, spacer + 3])

        if inst[0]:
            ret[0] = f"\033[94m{packinfo['info']['name']}=={inst[2]} already installled ({byteCalc(inst[1])})"

            return ret 
            
        addDependencies(f"{packinfo['info']['name']}=={inst[2]}", self.__dev)
        return ret
        

    def __remote_package(self, pack:str, http) -> dict:
        packName = pack.replace("=", ' ').replace(">", ' ').replace("<", ' ').replace("~", ' ').split(' ')[0]
    
        packinfo = http.request("GET", f"https://pypi.org/pypi/{packName}/json/")
            
        if packinfo.status == 404:
            Logger(f"Package {packName} not found", 'red')
            return {}

        packinfo = json.loads(packinfo.data.decode())

        if packinfo['urls'] == []:
            Logger(f"Package {packName} don't have a version for install", 'red')
            return {}

        pac = self.__installPackage(packinfo, http, pack)

        if pac == 'error':
            return
                
        if packinfo['info']['requires_dist']:
            Logger(f"\n{packName} dependencies:", 'yellow')

            self.__dependenciesLoop(packinfo['info']['requires_dist'], self.__dependencies, http, 3)
        
        Logger("\n")
        return packinfo


    def run(self, args:list) -> None:
        http = urllib3.PoolManager()
        
        commands = listArgsInstall(args)
        self.__dev = commands[1]
        self.__u = commands[2]

        for i in commands[0]:
            if self.__u:
                remove.Remover([pureDependency(i), '--yes'])
            
            res = self.__remote_package(i, http)

            if res == {}:
                continue