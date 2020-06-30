from Utils.versionControl import lessThan, moreThan, equals, equalSerie, combine, getVersions, byteCalc
import pkg_resources as pr
import subprocess
import itertools
import tempfile
import urllib3
import tarfile
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

        if not os.path.exists(temp + "/packsX"):
            os.mkdir(temp + "/packsX")

        self.run(args)


    def __normalizeVersion(self, version:str, res:list) -> list:
        version = version.replace(res['info']['name'].lower(), '')
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
    
    def __downloadPackage(self, url:str, filew:str, http) -> None:
        if os.path.exists(filew):
            return

        files = http.request("GET", url)

        with open(filew, "wb") as f:
            f.write(files.data)

    
    def __installPackageDependencies(self, res:dict, http, version:str) -> None:
        temp = tempfile.gettempdir()

        vers = self.__normalizeVersion(version, res)
        vers.pop()

        if vers == "ErrorR":
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
            return

        if vers == "ErrorV":
            return
        
        remote = [i for i in vers if i['url'].endswith('.whl')]

        if len(remote) == 0:
            return True

        else:
            remote = remote[0]
            self.__downloadPackage(remote['url'], temp + f"/packsX/{remote['filename']}", http)
            return self.__wheelInstall(res['info']['name'], temp + f"/packsX/{remote['filename']}")
        

    def __installPackage(self, res:dict, http, version:str) -> str:
        temp = tempfile.gettempdir()
        vers = self.__normalizeVersion(version, res)
        v = vers.pop()

        if vers == "ErrorR":
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
            return

        if vers == "ErrorV":
            return "error"
        
        remote = [i for i in vers if i['url'].endswith('.whl')][0]
        print(f"\n\033[92mPackage {res['info']['name']} found in version {v} ({byteCalc(remote['size'])})\033[37m")

        ### DOWNLOAD

        print(f"\033[95m\nDownloading {res['info']['name']}\033[37m", end='\r')
        self.__downloadPackage(remote['url'], temp + f"/packsX/{remote['filename']}", http)
        print(f"\033[92mDownload finish           \033[37m")

        ### INSTALL 
        print(f"\033[95m\nInstalling {res['info']['name']}\033[37m", end='\r')
        whl = self.__wheelInstall(res['info']['name'], temp + f"/packsX/{remote['filename']}")
        
        if not whl:
            print(f"\033[92m{res['info']['name']} was successfully installed \033[37m")

        else:
            print(f"\033[94m{res['info']['name']} already installled \033[37m")

        return remote


    def __dependencies(self, pack:str, http) -> str:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack.split(' ')[0]}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())

        inst = self.__installPackageDependencies(packinfo, http, pack)

        if inst:
            return f"\033[94m{packinfo['info']['name']}=={packinfo['info']['version']} already installled"
        
        return f"{packinfo['info']['name']}=={packinfo['info']['version']}"
        

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

            for i in packinfo['info']['requires_dist']:
                if ('; extra' in i): 
                    continue

                print(" " * 3, i.split(' ')[0], end="\r")
                
                a = self.__dependencies(i, http)
                
                print(" " * 3, f"\033[92m{a}\033[37m")

            print('\n')
        
        return packinfo


    def run(self, args:list):
        http = urllib3.PoolManager()

        for i in args[2:]:
            res = self.__remote_package(i, http)

            if res == {}:
                continue