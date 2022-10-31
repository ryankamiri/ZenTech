import urllib.request
import os
import sys
import subprocess
import base64
#from time import sleep
url = ""
urllib.request.urlretrieve(url + "checker.pyc", filename="checker.pyc")
urllib.request.urlretrieve(url + "config.ini", filename="config.ini")
urllib.request.urlretrieve(url + "info.ini", filename="info.ini")
urllib.request.urlretrieve(url + "roblopy.pyc", filename="roblopy.pyc")
urllib.request.urlretrieve(url + "setup.pyc", filename="setup.pyc")
urllib.request.urlretrieve(url + "updater.pyc", filename="updater.pyc")
urllib.request.urlretrieve(url + "readme.md", filename="readme.md")
print("Finished Updating")
python = sys.executable
script = os.path.realpath("checker.pyc")
subprocess.Popen([python, script])
print("Exiting Updater!")
sys.exit()
