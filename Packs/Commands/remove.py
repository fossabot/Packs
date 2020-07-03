import pkg_resources as pr
import platform
import sys
import os
import shutil


class Remover:
    def __init__(self, args:list):
        self.run(args)


    def __listScripts(self, binpath:str, script:str, gui:bool = False) -> list:
        e = binpath + script
        paths = [e]

        if platform.system().lower() == "windows":
            paths.append(e + ".exe")
            paths.append(e + '.exe.manifest')
            
            if gui:
                paths.append(e + '-script.pyw')

            else:
                paths.append(e + '-script.py')

        return paths


    def __validadePath(self, paths:list) -> list:
        valids = []

        for i in paths:
            if os.path.exists(i):
                valids.append(i)

        return valids

    
    def __removeFiles(self, paths: list) -> None:
        for i in paths:
            try:
                os.remove(i)

            except PermissionError:
                shutil.rmtree(i)

            except FileNotFoundError:
                pass


    def __getEnvScript(self) -> str:
        if os.path.exists(sys.prefix + "/bin"):
            return sys.prefix + "/bin/"

        else:
            return sys.prefix + "\\Scripts\\"


    def __eggRemove(self, dist:pr.Distribution) -> list:
        if dist.egg_info:
            d = dist.egg_info.replace('\\', '/').split('/')

            if d[len(d) - 1] == 'EGG-INFO':
                d.pop()

            return['/'.join(d)]
        return []


    def __showRecorded(self, dist:pr.Distribution) -> list:
        paths = []

        try:
            rec = dist.get_metadata_lines("RECORD")

            for i in rec:
                i = i.split(',')[0]

                if ".." in i:
                    continue

                i = i.split('/')

                if dist.location + "/" + i[0] not in paths:
                    paths.append(os.path.join(dist.location + "/", i[0]))

        except FileNotFoundError:
            paths = self.__eggRemove(dist)
            paths.append(dist.egg_info)
        

        return paths


    def __getFilesToRemove(self, dist:pr.Distribution) -> list:
        scriptsDir = self.__getEnvScript()
        paths = []

        console = dist.get_entry_map(group='console_scripts')
        gui = dist.get_entry_map(group='gui_scripts')

        paths.extend(self.__showRecorded(dist))

        for i in console.keys():
            paths.extend(self.__listScripts(scriptsDir, i))

        for i in gui.keys():
            paths.extend(self.__listScripts(scriptsDir, i, True))

        paths = self.__validadePath(paths)

        for i in paths:
            print(" " * 3, i)

        return paths


    def run(self, args:list) -> None:
        print('\n')
        for i in args[2:]:
            try:
                dis = pr.get_distribution(i)
            
            except pr.DistributionNotFound:
                print(f"\033[91mERROR: package {i} not found\033[37m")
                continue

            print(f"\033[93mDo you want to remove {i} [y, n]\033[37m")

            paths = self.__getFilesToRemove(dis)
            opt = input(">>> ")

            if opt == 'y':
                self.__removeFiles(paths)
                print(f"\033[92m{i} was successfully removed\033[37m")


            print('\n')
