#!/bin/bash

clear_cache(){
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete
}

install(){
    echo "install..."
    pip install -r requirements.txt
    echo "install done"
}

exit_code=0

ut(){
    echo "test app"
    python manage.py test --settings boxing_app.app_settings boxing_app.tests
    exit_code1=$?
    echo "api test result: $exit_code1"

    echo "test biz"
    python manage.py test --settings boxing_app.app_settings biz
    exit_code2=$?
    echo "biz test result: $exit_code2"

    echo "test console"
    python manage.py test --settings boxing_console.console_settings boxing_console.tests
    exit_code3=$?
    echo "console test result: $exit_code3"

    exit_code=`expr $exit_code1 + $exit_code2 + $exit_code3`
}

clear_cache && install && ut

exit $exit_code
