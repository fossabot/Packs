import pkg_resources as pr
import platform
import shutil
import sys
import os

try:
    from Packs.Utils.cliControl import listArgsRemove, pureDependency
    from Packs.Utils.dependenciesControl import removeDependency, openToCreate
    from Packs.Utils.logger import Logger
    
except (ModuleNotFoundError, ImportError):
    from Utils.cliControl import listArgsRemove, pureDependency
    from Utils.dependenciesControl import removeDependency, openToCreate
    from Utils.logger import Logger


class Remover:
    def __init__(self, args:list, cli=False):
        openToCreate()
        if cli:
            self.run(args[2:])

        else:
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

    
    def __removeFiles(self, paths: list, dist:pr.Distribution) -> None:
        for i in paths:
            if os.path.isdir(i):
                shutil.rmtree(i)
                continue

            try:
                os.remove(i)

            except FileNotFoundError:
                pass
        
        removeDependency(f"{dist.key}=={dist.version}")


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
            Logger(f"{' ' * 3} {i}")

        return paths


    def run(self, args:list) -> None:
        comm = listArgsRemove(args)

        commands = comm[0]
        yes = comm[1]

        Logger()
        for i in commands:
            i = pureDependency(i)

            try:
                dis = pr.get_distribution(i)
            
            except pr.DistributionNotFound:
                Logger(f"ERROR: package {i} not found", 'red')
                continue

            Logger(f"Do you want to remove {i} [y, n]", 'yellow')

            paths = self.__getFilesToRemove(dis)
            
            if yes:
                self.__removeFiles(paths, dis)
                print(f"{i} was successfully removed\n", 'green')
                continue

            opt = input(">>> ")

            if opt == 'y':
                self.__removeFiles(paths, dis)
                Logger(f"{i} was successfully removed", 'green')


            print()
