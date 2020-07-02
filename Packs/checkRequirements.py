import subprocess

try:
    import urllib3

except ModuleNotFoundError:
    print("\033[91mUrllib3 Not installed. We will install for you ;)\033[37m")
    subprocess.run(['pip', 'install', 'urllib3'], stdin=None, stdout=None)