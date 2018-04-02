#!/bin/bash

# CUR_DIR=$(dirname $(readlink -f $0))
CUR_DIR=/opt/pulsewallet
WORK_DIR=$CUR_DIR/pulsewallet
PROJ_NAME=pulsewallet
LOGDIR=/var/log/pulsewallet
USER=pulsewallet
PYTHON=python2.7
VENV=$CUR_DIR/venv
GUNICORN=$VENV/bin/gunicorn
GUNICORN_WORKER=
# GUNICORN_WORKER="--worker-class eventlet"

initsudoecho() {
    # init sudo
    sudo echo "" > /dev/null
}

cmd=$1; ! [ -z "$cmd" ] && shift
param1=$1; ! [ -z "$param1" ] && shift

checkps=`ps ax | grep gunicorn | grep -v grep | grep -v sudo`

setup() {
    initsudoecho

    # creating log dir and force set permissions
    ! [ -d "$LOGDIR" ] && sudo mkdir -p $LOGDIR
    sudo chown -R $USER: $LOGDIR
    sudo chmod -R a+rwX $LOGDIR

    sudo -u $USER sh -c "cd $WORK_DIR; . $VENV/bin/activate; $PYTHON $WORK_DIR/manage.py collectstatic --noinput"
}


case $cmd in
    setup)
        setup
        ;;
    start)
        if [ -n "$checkps" ]; then
            echo "gunicorn seems to be already running"
            exit 133
        fi

        setup

        APPPARAMS=""
        DAEMONFLAG="-D"
        STARTMSG="daemon"
        [ "$param1" = "--debug" ] && DAEMONFLAG="" && APPPARAMS="debug=True" && STARTMSG="interactive"

        sudo -u $USER sh -c "cd $WORK_DIR; . $VENV/bin/activate; $PYTHON $GUNICORN -c $CUR_DIR/config/gunicorn/gunicorn.conf.py $GUNICORN_WORKER '$PROJ_NAME.wsgi:application' $DAEMONFLAG"
        if [ $? -ne 0 ]; then
            echo "ERROR starting gunicorn"
            exit 127
        else
            echo "Started $STARTMSG"
        fi

        sudo service nginx restart
        ;;
    stop)
        if [ -z "$checkps" ]; then
            echo "gunicorn seems to be already stopped"
            # exit 132
        else
            initsudoecho
            ps ax | grep gunicorn | grep -v grep | grep -v sudo | awk '{print $1}' | xargs -r sudo kill -9
            echo "gunicorn killed"
        fi
        ;;
    reload)
        initsudoecho
        ps ax | grep gunicorn | grep -v grep | grep -v sudo | awk '{print $1}' | xargs -r sudo kill -s HUP
        sudo service nginx reload
        ;;
    help)
        echo "Run parameters:"
        echo "    manage.sh help                  - this help"
        echo "    manage.sh setup                 - just create user/dirs/permissions"
        echo "    manage.sh start [--debug]       - with '--debug' gunicorn will be run in not-daemon mode"
        echo "    manage.sh stop"
        echo "    manage.sh reload                - soft reload"
        ;;
    *)
        echo "ERROR, wrong parameter"
        exit 1
esac

