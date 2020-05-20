import requests
import json

def release():
    resp = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").text
    response = json.loads(resp)
    return [response["latest"]["snapshot"], response["latest"]["release"]]