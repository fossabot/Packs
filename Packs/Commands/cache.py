import tempfile
import shutil
import os


try:
    from Packs.Utils.logger import Logger

except (ImportError, ModuleNotFoundError):
    from Utils.logger import Logger


class Cacher:
	def __init__(self, args, cli=False):
		if cli:
			self.run(args[2:])

		else:
			self.run(args)


	def __clear(self) -> None:
		temp = tempfile.gettempdir()

		if os.path.exists(os.path.join(temp, "packsX")):
			shutil.rmtree(os.path.join(temp, "packsX"))

		Logger("\nCache cleared\n", 'green')


	def __list(self) -> None:
		temp = tempfile.gettempdir()

		if os.path.exists(os.path.join(temp, "packsX")):
			for i in os.listdir(os.path.join(temp, "packsX")):
				s = i.split("-")

				package = s[0].replace("_", " ")
				version = s[1]

				Logger(f"{package}=={version:8}", 'green')
			return

		Logger("\nNo cache\n", "yellow")


	def run(self, args:list) -> None:
		if len(args) > 1:
			Logger("\nOnly one flag is supported\n", "red")
			return

		flags = {
			"-c": self.__clear,
			"-l": self.__list
		}

		try:
			flags[args[0]]()

		except KeyError:
			Logger("\nThis flag is not supported\n", "red")


