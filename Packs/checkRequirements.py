
import subprocess
import json


try:
    import urllib3

except ModuleNotFoundError:
    print("\033[91mUrllib3 Not installed. We will install for you ;)\033[37m")
    subprocess.run(['pip', 'install', 'urllib3'], stdin=None, stdout=None)

try:
	from __init__ import __version__
	
except (ModuleNotFoundError, ImportError):
	from Packs import __version__


current = int(''.join(__version__.split('.')))

http = urllib3.PoolManager()

packsV = http.request('GET', 'https://pypi.org/pypi/Packs/json')
von = json.loads(packsV.data)['info']['version']
packsV = int("".join(von.split('.')))


if current < packsV:
    print(f"\033[93mYour version of Packs is {__version__}, you can upgrade to version {von} using the command: packs i packs -u\033[37m")