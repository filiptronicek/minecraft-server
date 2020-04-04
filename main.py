import os
import shutil
import subprocess

import requests
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))
server_dir = dir_path + "/server/"

""" Description
    :type file:
    :param file:
    
    :type word:
    :param word: - what should be replaced
    
    :type replacement:
    :param replacement: - with what the word should be replaced
    
    :raises:
    
    :rtype:
"""


def find_and_replace(file_, word, replacement):
    with open(file_, "r+") as f:
        text = f.read()
        f.write(text.replace(word, replacement))


def setup():
    server_name = input("What is the server's name? ")
    os.chdir(server_dir)
    bat_file = open(server_dir + "start.bat", "w")
    bat_file.write("java -Xmx2048M -Xms1024M -jar server.jar nogui")
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


def get_server_jar_url(version_):
    """
    Gets the latest server.jar for specified Minecraft version
    :param version_: Minecraft version
    :return: Download url in the form of https://launcher.mojang.com/v1/objects/.../server.jar
    """
    versions_manifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    version_manifest = list(filter(lambda a: a["id"] == version_, versions_manifest["versions"]))[0]
    download_url = requests.get(version_manifest["url"]).json()
    return download_url["downloads"]["server"]["url"]


if not os.path.exists("server/server.jar"):
    chunk_size = 1024

    version = input("Please send what version of Minecraft you want to use: ")

    url = get_server_jar_url(version)

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
