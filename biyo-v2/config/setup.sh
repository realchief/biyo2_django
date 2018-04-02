#!/bin/sh

# THIS FILE intended to be run line-by-line by hands!
# Don't run it automatically!
# In case of session interruption - start from the beginning (use 'screen -D -R')
# Verified on Ubuntu 14.04

# this line for manual run only!
CUR_DIR=`pwd`
# for automatic run use this line
CUR_DIR=$(dirname $(readlink -f $0))

PROJECT=pulsewallet
BASE_DIR=/opt/pulsewallet
PROJ_USER=pulsewallet
PYTHON=python2.7
PIP=pip2

sudo adduser $PROJ_USER
sudo adduser $PROJ_USER sudo

# directories/permissions
sudo mkdir -p $BASE_DIR
sudo mkdir -p $BASE_DIR/media
sudo mkdir -p $BASE_DIR/static
sudo chown -R $PROJ_USER: $BASE_DIR
sudo chmod -R a+rwX $BASE_DIR
sudo chmod -R -t $BASE_DIR

sudo chmod a+rwX /tmp
sudo chmod -t /tmp


sudo service apache2 stop
sudo update-rc.d -f apache2 disable

sudo apt-get update
sudo apt-get install -y git nginx mc htop
sudo apt-get install -y mysql-client mysql-server
sudo apt-get install -y $PYTHON $PYTHON-dev

# install pip
cd /tmp/
wget https://bootstrap.pypa.io/get-pip.py
sudo $PYTHON get-pip.py
cd -

sudo $PIP install ipython
sudo pip install virtualenv

sudo apt-get install -y libmysqlclient-dev


cd $BASE_DIR
virtualenv venv
source venv/bin/activate

# HERE: checkout project to the folder 'pulsewallet'

# fix permissions if were broken
sudo chown -R $PROJ_USER: $BASE_DIR
sudo chmod -R a+rwX $BASE_DIR
sudo chmod -R -t $BASE_DIR

# TODO: fix permissions for '.git' folder

$PIP install -r pulsewallet/config/pip/requirements.txt

# install nginx config
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s $BASE_DIR/config/nginx/pulsewallet_passwd /etc/nginx/
sudo ln -s $BASE_DIR/config/nginx/pulsewallet.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/pulsewallet.conf /etc/nginx/sites-enabled/

sudo service nginx restart
