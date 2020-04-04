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


if not os.path.exists("server/server.jar"):
    chunk_size = 1024
    url = "https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar"

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
