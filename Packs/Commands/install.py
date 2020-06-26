import subprocess
import itertools
import tempfile
import urllib3
import tarfile
import shutil
import wheel
import json
import os
import sys

class Installer:
    def __init__(self, args:list):
        self.run(args)


    def normalizeVersion(self, version:str, res:list) -> list:
        if version:
            if "==" in version:
                vx = version.replace("==", "").replace("(", '').replace(")", '')
                remote = [i for i in res['releases'][f'{vx}'] if i['url'].endswith('.tar') or i['url'].endswith('.tar.gz')][0]
                print(remote)

            else:
                vx = version.replace("(", '').replace(")", '')
        

    def installPackage(self, res:dict, http, version:str) -> None:
        v = res['info']['version']

        # self.normalizeVersion(version, res)

        remote = [i for i in res['releases'][f'{v}'] if i['url'].endswith('.tar') or i['url'].endswith('.tar.gz')][0]

        # print(f"\033[95m\nDownloading {res['info']['name']}\033[37m")
        files = http.request("GET", remote['url'])
        temp = tempfile.gettempdir()

        with open(temp + f"/{remote['filename']}", "wb") as f:
            f.write(files.data)

        # print(f"\n\033[92mDownload finish           \033[37m")
        
        path = f"{temp}/{res['info']['name'].replace('-', '_')}-{v}\\"

        with tarfile.open(temp + f"/{remote['filename']}", "r:gz") as tar:
            tar.extractall(temp)

        os.chdir(path)
        FNULL = open(os.devnull, 'w')

        
        subprocess.run(['python', 'setup.py', 'install'], stdout=FNULL, stderr=subprocess.PIPE)


    def dependencies(self, pack:str, http) -> str:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack.split(' ')[0]}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())

        ver = pack.split(' ')
        self.installPackage(packinfo, http, ver[1] if len(ver) > 1 else None)
        
        return f"{packinfo['info']['name']}=={packinfo['info']['version']}"
        

    def remote_package(self, pack:str, http) -> dict:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack}/json/")
            
        if packinfo.status == 404:
            print(f"\n\033[91mPackage {pack} not founded\033[37m")
            return {}
        
        packinfo = json.loads(packinfo.data.decode())
        print(f"\n\033[92mPackage {pack} founded in version {packinfo['info']['version']}\033[37m")
        
        if packinfo['info']['requires_dist']:
            print(f"\n\033[93m{pack} dependencies:\033[37m")

            for i in packinfo['info']['requires_dist']:
                if ('; extra' in i): 
                    continue

                print(" " * 3, i.split(' ')[0], end="\r")
                
                a = self.dependencies(i, http)
                
                print(" " * 3, f"\033[92m{a}\033[37m")

            print('\n')
        
        self.installPackage(packinfo, http, None)
        print("SADAS")
        return packinfo


    def run(self, args:list):
        http = urllib3.PoolManager()

        for i in args[2:]:
            res = self.remote_package(i, http)

            if res == {}:
                continue