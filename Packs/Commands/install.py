from Utils.versionControl import lessThan, moreThan, equals, equalSerie, combine, getVersions
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
        self.run(args)


    def __normalizeVersion(self, version:str, res:list) -> list:
        version = version.replace(res['info']['name'], '')
        releases = res['releases']

        versionControl = {
            "<": lessThan,
            "==": equals,
            '~': equalSerie,
            '>': moreThan,
        }

        if version:
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

        l = sorted(releases, key=lambda x: releases[x][0]['upload_time'])
        rels = getVersions(l, releases)
        
        c = combine([rels])
        c = c[len(c) - 1]

        return c


    def __wheelInstall(self, name:str, filewhl:str) -> None:
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

    
    def __downloadPackage(self, url:str, filew:str, http) -> None:
        files = http.request("GET", url)

        with open(filew, "wb") as f:
            f.write(files.data)

    
    def __installPackageDependencies(self, res:dict, http, version:str) -> None:
        temp = tempfile.gettempdir()

        vers = self.__normalizeVersion(version, res)

        if vers == "ErrorR":
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
            return

        if vers == "ErrorV":
            return

        remote = [i for i in vers[:1] if i['url'].endswith('.whl')][0]

        self.__downloadPackage(remote['url'], temp + f"/{remote['filename']}", http)
        self.__wheelInstall(res['info']['name'], temp + f"/{remote['filename']}")
        

    def __installPackage(self, res:dict, http, version:str) -> str:
        temp = tempfile.gettempdir()
        vers = self.__normalizeVersion(version, res)

        if vers == "ErrorR":
            print("\033[91mERROR there is no version that satisfies the condition\033[37m")
            return

        if vers == "ErrorV":
            return

        print(f"\n\033[92mPackage {res['info']['name']} found in version {vers[len(vers) - 1]}\033[37m")
        
        remote = [i for i in vers[:1] if i['url'].endswith('.whl')][0]

        ### DOWNLOAD

        print(f"\033[95m\nDownloading {res['info']['name']}\033[37m", end='\r')
        self.__downloadPackage(remote['url'], temp + f"/{remote['filename']}", http)
        print(f"\033[92mDownload finish           \033[37m")

        ### INSTALL 

        self.__wheelInstall(res['info']['name'], temp + f"/{remote['filename']}")
        return remote


    def __dependencies(self, pack:str, http) -> str:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack.split(' ')[0]}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())

        ver = pack.split(' ')
        self.__installPackageDependencies(packinfo, http, ver[1] if len(ver) > 1 else None)
        
        return f"{packinfo['info']['name']}=={packinfo['info']['version']}"
        

    def __remote_package(self, pack:str, http) -> dict:
        packName = pack.replace("=", ' ').replace(">", ' ').replace("<", ' ').replace("~", ' ').split(' ')[0]
    
        packinfo = http.request("GET", f"https://pypi.org/pypi/{packName}/json/")
            
        if packinfo.status == 404:
            print(f"\n\033[91mPackage {packName} not found\033[37m")
            return {}

        packinfo = json.loads(packinfo.data.decode())
        self.__installPackage(packinfo, http, pack)
                
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