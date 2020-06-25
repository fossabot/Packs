import tempfile
import urllib3
import tarfile
import json
import os
import sys

class Installer:
    def __init__(self, args:list):
        self.run(args)


    def installPackage(self, res:dict, http) -> None:
        v = res['info']['version']

        remote = [i for i in res['releases'][f'{v}'] if i['url'].endswith('.tar') or i['url'].endswith('.tar.gz')][0]

        files = http.request("GET", remote['url'])

        temp = tempfile.gettempdir()

        with open(temp + f"/{remote['filename']}", "wb") as f:
            f.write(files.data) 

        print(temp + f"\\{remote['filename']}")

        tar = tarfile.open(temp + f"\\{remote['filename']}", 'r:gz')
        tar.extractall(temp)

        print(temp + f"\\{remote['filename'].replace('.tar.gz', '')}")
        print(os.path.isdir(temp + f"\\{remote['filename'].replace('.tar.gz', '')}"))

        tar.close() 

        sys.path.insert(1, temp + f"\\{remote['filename'].replace('.tar.gz', '')}")
        os.system(f"python {temp}\\{remote['filename'].replace('.tar.gz', '')}\\setup.py install")

        print(res['releases'][f'{v}'][0]['url'])


    def dependencies(self, pack:str, http) -> str:
        packinfo = http.request("GET", f"https://pypi.org/pypi/{pack}/json/")

        if packinfo.status == 404:
            return "error"

        packinfo = json.loads(packinfo.data.decode())

        self.installPackage(packinfo, http)
        
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
                
                a = self.dependencies(i.split(' ')[0], http)
                
                print(" " * 3, f"\033[92m{a}\033[37m")

            print('\n')
        
        self.installPackage(packinfo, http)
        return packinfo


    def run(self, args:list):
        http = urllib3.PoolManager()

        for i in args[2:]:
            res = self.remote_package(i, http)

            if res == {}:
                continue