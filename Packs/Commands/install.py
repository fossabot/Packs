from Utils.versionControl import (lessThan, moreThan, equals, byteCalc, combine, equalSerie, validVersionPython)
from Utils.dependenciesControl import addDependencies, openToCreate
from Utils.cliControl import listArgsInstall
from typing import Callable
import pkg_resources as pr
import subprocess
import itertools
import tempfile
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
    print("\n\033[91mPlease activate the virtual environment to use Packs\n\033[37m")
    sys.exit(0)


class Installer:
    def __init__(self, args:list):
        temp = tempfile.gettempdir()
        self.__deps = []
        self.__dev = False
        openToCreate()

        if not os.path.exists(temp + "/packsX"):
            os.mkdir(temp + "/packsX")

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
            pr.get_distribution(name)

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
        return True


    def __tarInstall(self, name:str, filewhl:str) -> bool:
        temp = tempfile.gettempdir()

        try:
            pr.get_distribution(name)

        except Exception:
            with tarfile.open(filewhl, 'r:gz') as tar:
                tar.extractall(temp + "/packsX")

            os.chdir(filewhl.replace(".tar.gz", ''))

            FNULL = open(os.devnull, 'w')

            subprocess.run(['python', 'setup.py', 'install'], stdout=FNULL, stderr=subprocess.PIPE)
            return False

        return True


    def __checkTypeInstallation(self, vers:list) -> list:
        remote = [i for i in vers if i['url'].endswith('.whl')]

        if len(remote) == 0:
            return [vers[0], self.__tarInstall]

        else:
            return [remote[0], self.__wheelInstall]

    
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
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
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
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
            return

        if vers == "ErrorV":
            return "error"
        
        remote = self.__checkTypeInstallation(vers)

        print(f"\n\033[92mPackage {res['info']['name']} found in version {v} ({byteCalc(remote[0]['size'])})\033[37m")
        addDependencies(f"{res['info']['name']}=={v}", self.__dev)

        ### DOWNLOAD

        print(f"\033[95m\nDownloading {res['info']['name']}\033[37m", end='\r')
        self.__downloadPackage(remote[0]['url'], temp + f"/packsX/{remote[0]['filename']}", http)
        print(f"\033[92mDownload finish           \033[37m")

        ### INSTALL 
        print(f"\033[95m\nInstalling {res['info']['name']}\033[37m", end='\r')
        whl = remote[1](res['info']['name'], temp + f"/packsX/{remote[0]['filename']}")
        
        if not whl:
            print(f"\033[92m{res['info']['name']} was successfully installed \033[37m")

        else:
            print(f"\033[94m{res['info']['name']} already installled \033[37m")

        return remote[0]


    def __dependenciesLoop(self, reqs:list, fun:Callable, http, spacer:int = 3):
        for i in reqs:
            if '; extra' in i or i.split(' ')[0] in self.__deps or "and extra" in i: 
                continue
            
            if "; python_version" in i and not validVersionPython(i.split("; python_version ")[1].replace('"', '')):
                continue

            i = i.split(" ; ")[0]
            self.__deps.append(i.split(' ')[0])

            print(" " * spacer, i.split(' ')[0], end="\r")
            
            a = fun(i, http, spacer)
            
            print(" " * spacer, f"\033[92m{a[0]}\033[37m")

            if len(a) > 1:
                a[1](*a[2])

    
    def __dependencies(self, pack:str, http, spacer:int) -> list:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack.split(' ')[0]}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())
        inst = self.__installPackageDependencies(packinfo, http, pack)

        ret = [f"{packinfo['info']['name']}=={inst[2]} ({byteCalc(inst[1])})"]

        addDependencies(f"{packinfo['info']['name']}=={inst[2]}", self.__dev)

        if packinfo['info']['requires_dist']:
            ret.append(self.__dependenciesLoop)
            ret.append([packinfo['info']['requires_dist'], self.__dependencies, http, spacer + 3])

        if inst[0]:
            ret[0] = f"\033[94m{packinfo['info']['name']}=={inst[2]} already installled ({byteCalc(inst[1])})"

            return ret 
            
        return ret
        

    def __remote_package(self, pack:str, http) -> dict:
        packName = pack.replace("=", ' ').replace(">", ' ').replace("<", ' ').replace("~", ' ').split(' ')[0]
    
        packinfo = http.request("GET", f"https://pypi.org/pypi/{packName}/json/")
            
        if packinfo.status == 404:
            print(f"\n\033[91mPackage {packName} not found\033[37m")
            return {}

        packinfo = json.loads(packinfo.data.decode())
        pac = self.__installPackage(packinfo, http, pack)

        if pac == 'error':
            return
                
        if packinfo['info']['requires_dist']:
            print(f"\n\033[93m{packName} dependencies:\033[37m")

            self.__dependenciesLoop(packinfo['info']['requires_dist'], self.__dependencies, http, 3)
        
        print("\n")
        return packinfo


    def run(self, args:list):
        http = urllib3.PoolManager()
        
        commands = listArgsInstall(args[2:])
        self.__dev = commands[1]

        for i in commands[0]:
            res = self.__remote_package(i, http)

            if res == {}:
                continue