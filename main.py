import os
import shutil
import subprocess
from typing import Optional, Any

import requests
from tqdm import tqdm

from versions.paper_mc import PaperMC
from versions.vanilla import Vanilla

dir_path = os.path.dirname(os.path.realpath(__file__))
server_dir = dir_path + "/server/"

versions = [Vanilla, PaperMC]


def find_and_replace(file_, word, replacement):
    with open(file_, "r+") as f:
        text = f.read()
        f.write(text.replace(word, replacement))


def setup():
    server_name = input("What is the server's name? ")
    os.chdir(server_dir)
    bat_file = open(server_dir + "start.bat", "w")
    bat_file.write("java -Xmx1024M -Xms1024M -jar server.jar nogui")
    bat_file.close()
    subprocess.call(server_dir + "start.bat")
    find_and_replace(server_dir + "eula.txt", "false", "true")
    print("Agreed to EULA")
    try:
        find_and_replace(
            server_dir + "server.properties",
            "motd=A Minecraft Server",
            "motd=" + server_name,
        )
    except Exception as err:
        print(f"failed, for some reason ({str(err)})")
    answer_start = input(
        "Wanna start the server right away or change the settings first? [start/conf]"
    )

    def ask_option():
        if answer_start == "start":
            subprocess.call(server_dir + "start.bat")
        elif answer_start == "conf":
            os_command_string = "notepad.exe server.properties"
            os.system(os_command_string)
        else:
            ask_option()

    ask_option()


def default_input(prompt: str, default: Optional[Any], strip: bool = True):
    resp = input(prompt)
    if len(resp) != 0:
        return resp.strip() if strip else resp
    return default


if not os.path.exists("server/server.jar"):
    chunk_size = 1024

    server_type = default_input("Choose server type (Vanilla or PaperMC, by default vanilla): ", "vanilla").lower()
    assert server_type in map(lambda ver: ver.__name__.lower(), versions)

    version = default_input("Please send what version of Minecraft you want to use (default 1.15.2): ", "1.15.2")

    url = list(filter(lambda a: a.__name__.lower() == server_type, versions))[0]().get_download_url(version)

    req = requests.get(url, stream=True)
    total_size = int(req.headers["content-length"])

    if not os.path.isdir("server/"):
        os.mkdir("server")

    with open("server.jar", "wb") as file:
        for data in tqdm(
            iterable=req.iter_content(chunk_size=chunk_size),
            total=total_size / chunk_size,
            unit="KB",
        ):
            file.write(data)
    shutil.move(dir_path + "/server.jar", server_dir + "server.jar")
    setup()
else:
    if os.path.isdir("server/logs"):
        os.chdir(server_dir)
        print("World Exists, starting server....")
        subprocess.call("start.bat")
    else:
        setup()
