import pkg_resources as pr

try:
	from Packs.Utils.cliControl import listArgsList
	from Packs.Utils.logger import Logger

except (ModuleNotFoundError, ImportError):
	from Utils.cliControl import listArgsList
	from Utils.logger import Logger


class Lister:
	def __init__(self, commands, cli=False):
		if cli:
			self.run(commands[2:])
			
		else:
			self.run(commands)


	def __drawer(self, packs:list, noPacks:list, color:bool, freeze:bool) -> None:
		for i in packs:
			if i.key.lower() in noPacks:
				continue

			name = f"\033[94m{i.key}\033[37m"

			if color:
				name = i.key

			if freeze:
				print(f"{name}=={i.version}")

			else:
				print(f"{name:45}\t{i.version}")


	def run(self, commands):
		packs = pr.working_set

		commands = listArgsList(commands)

		color = commands[2]
		freeze = commands[1]

		noPacks = ['wheel', 'pkg_resources', 'pip', 'setuptools']

		if commands[3]:
			return [i.key for i in packs if i.key.lower() not in noPacks]

		self.__drawer(packs, noPacks, color, freeze)
		