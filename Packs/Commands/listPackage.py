import pkg_resources as pr

try:
	from Packs.Utils.cliControl import listArgsList

except ModuleNotFoundError:
	from Utils.cliControl import listArgsList


class Lister:
	def __init__(self, commands):
		self.run(commands)


	def run(self, commands):
		packs = pr.working_set

		commands = listArgsList(commands[2:])

		color = commands[2]
		freeze = commands[1]

		noPacks = ['wheel', 'pkg_resources', 'pip', 'setuptools']

		for i in packs:
			if i.key.lower() in noPacks:
				continue

			name = f"\033[94m{i.key}\033[37m"

			if color:
				name = i.key

			if freeze:
				print(f"{name}=={i.version}")

			else:
				print(f"{name:25}\t{i.version}")