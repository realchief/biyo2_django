#!/bin/bash
# Build pulsewallet

# PYTHON=/usr/bin/python

CUR_DIR=$(dirname $(readlink -f $0))

PYTHON=$CUR_DIR/venv/bin/python

cmd=$1; ! [ -z "$cmd" ] && shift
[ -z "$cmd" ] && cmd="dev"
param1=$1; ! [ -z "$param1" ] && shift

django_build() {
    # compile locales
    $PYTHON $CUR_DIR/backend/manage.py compilemessages

    # collect static files
    $PYTHON $CUR_DIR/backend/manage.py collectstatic --noinput
}

case $cmd in
dev)
    django_build

;;
prod)
    django_build

;;
esac
