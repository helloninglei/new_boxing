#!/bin/bash

clear_cache(){
    find . -type d -name "__pycache__" | xargs rm -rf
}

install(){
    echo "install..."
    pip3 install -r requirements.txt
    echo "install done"
}


migrate(){
    echo "migrate..."
    python manage.py migrate --noinput --settings boxing_app.app_settings
    echo "migrate done"
}

deploy(){
    mkdir -p /var/log/new_boxing
    /etc/init.d/supervisord restart
    /usr/local/bin/gunicorn $APP.wsgi:application -c /work/deploy/config.py
}

cd /work && clear_cache && install && migrate && deploy
