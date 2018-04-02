#!/bin/sh

DBROOTUSER=root
DB_USER=biyo
DB_PASS=biyo
DB_NAME=biyo_dev
DUMP_FILE=/opt/biyo_bump.sql

# create user and database
echo "create database $DB_NAME; grant all on $DB_NAME.* to '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';FLUSH PRIVILEGES;" | mysql -u $DBROOTUSER --password

# load db dump
cat $DUMP_FILE | mysql -u $DB_USER --password -D $DB_NAME
