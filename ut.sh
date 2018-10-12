#!/bin/bash

function clear_cache(){
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete
}

function install(){
    echo "install..."
    pip install -r requirements.txt
    echo "install done"
}

exit_code=0

function ut(){
    echo "test app"
    pytest --ds=boxing_app.app_settings boxing_app/tests --no-migrations --disable-warnings
    exit_code1=$?
    echo "app test result: $exit_code1"

    echo "test biz"
    pytest --ds=boxing_app.app_settings biz/tests --no-migrations --disable-warnings
    exit_code2=$?
    echo "biz test result: $exit_code2"

    echo "test console"
    pytest --ds=boxing_console.console_settings boxing_console/tests --no-migrations --disable-warnings
    exit_code3=$?
    echo "console test result: $exit_code3"

    exit_code=`expr $exit_code1 + $exit_code2 + $exit_code3`
}

clear_cache && install && ut

exit $exit_code
