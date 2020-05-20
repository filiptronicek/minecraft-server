import requests
import json

def release():
    resp = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").text
    responce = json.loads(resp)
    return [responce["latest"]["snapshot"], responce["latest"]["release"]]