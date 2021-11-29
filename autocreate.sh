apt update
apt upgrade

# install docker
apt install docker.io

# download the Minecraft world with wget, and extract it
if [ -n "$1" ]; then
    wget $1
    tar -xvf *.tar.gz
    rm *.tar.gz
fi

# run the server
docker run -d -v /root:/data \
    -e TYPE=SPIGOT \
    -e EULA=TRUE --name mc itzg/minecraft-server \
    -p 25565:25565
