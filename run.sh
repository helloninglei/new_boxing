#!/bin/bash

# 在docker容器内运行uwsgi

clear_cache(){
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete
}

install(){
    echo "install..."
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    echo "install done"
}


migrate(){
    echo "migrate..."
    python manage.py migrate --noinput --settings boxing_app.app_settings
    echo "migrate done"
}

deploy(){
    /usr/local/bin/uwsgi /etc/uwsgi.ini
}

cd /work && clear_cache && install && migrate && deploy
