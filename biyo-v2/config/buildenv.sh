#!/bin/sh

if type "greadlink" > /dev/null; then
    alias readlink='greadlink';
    echo "Using greadlink";
fi

CUR_DIR=$(dirname $(dirname $(readlink -f $0)))

echo Creating venv environment
virtualenv --no-site-packages $CUR_DIR/venv

echo Install PIP inside virtual environment
$CUR_DIR/venv/bin/easy_install pip

echo Installing dependencies to venv environment
env ARCHFLAGS="-arch x86_64" $CUR_DIR/venv/bin/pip install -r $CUR_DIR/config/pip/requirements.txt
