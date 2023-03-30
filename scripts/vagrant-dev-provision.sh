#!/bin/bash

cd $HOME

apt update

apt install -y --no-install-recommends build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
python3-dev libnacl-dev libopus-dev libopus0 libopusenc-dev wget git unzip tar

sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

apt-get update
apt-get install -y redis postgresql-15 postgresql-client-15

# systemctl enable --now redis-server
# systemctl enable --now postgresql-server

wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz 
tar xvf Python-3.11.2.tgz 
cd Python-3.11.2  

./configure --with-ensurepip=install
make -j 8
make altinstall

python --version
pip install --upgrade pip setuptools wheel

curl -sSL https://install.python-poetry.org | python -
export PATH="$PATH:/$HOME/.local/bin"
echo export PATH="$PATH:/$HOME/.local/bin" >> ~/.bashrc

cd $HOME/Kumiko
poetry install