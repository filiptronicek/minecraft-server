from tqdm import tqdm
import requests
import os, subprocess
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
server_dir = dir_path+"/server/"

def find_and_replace(file, word, replacement):
  with open(file, 'r+') as f:
    text = f.read()
    f.write(text.replace(word, replacement))

def setup():
    os.chdir(server_dir)
    bat_file = open(server_dir+"start.bat","w")
    bat_file.write("java -Xmx2048M -Xms1024M -jar server.jar nogui") 
    bat_file.close()
    subprocess.call(server_dir+"start.bat")
    find_and_replace(server_dir+"eula.txt", "false", "true")
    print("Agreed to EULA")
    answerStart = input("Wanna start the server right away or change the settings first? [start/conf]")
    def askOption():
        if answerStart == "start":
            subprocess.call(server_dir+"start.bat")
        elif answerStart == "conf":
            osCommandString = "notepad.exe server.properties"
            os.system(osCommandString)
        else:
            askOption()    
    askOption()

if(os.path.exists("server/server.jar") == False):

    chunk_size = 1024
    url = "https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar"

    req = requests.get(url, stream = True)
    total_size = int(req.headers['content-length'])

    if os.path.isdir("server/") == False:
        os.mkdir("server")

    with open("server.jar", "wb") as file:
        for data in tqdm(iterable=req.iter_content(chunk_size=chunk_size), total = total_size/chunk_size, unit='KB'):
            file.write(data)
    shutil.move(dir_path+"/server.jar",server_dir+"server.jar")
    setup()
else:
    if os.path.isdir("server/logs"):
         os.chdir(server_dir)
         print("World Exists, starting server....")
         subprocess.call("start.bat")
    else:
         setup()
