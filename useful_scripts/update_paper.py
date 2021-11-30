import requests
import re
import json
import os

req = requests.get("https://papermc.io/api/v2/projects/paper/version_group/1.18/builds").text

releases = json.loads(req)

download = 'https://papermc.io/api/v2/projects/paper/versions/'+releases['builds'][-1]['version'] + '/builds/' + str(releases['builds'][-1]['build']) + '/downloads/'+releases['builds'][-1]['downloads']['application']['name']

print("Removing old Paper...")
os.system('rm paper.jar')
print("Removed")
print()
print("Downloading new Paper")
os.system('wget -O paper.jar ' + download)