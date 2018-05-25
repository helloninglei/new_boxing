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
# 仅开发环境用
#    python manage.py loaddata user --settings boxing_app.app_settings
#    python manage.py loaddata hot_video --settings boxing_app.app_settings
}

deploy(){
    /usr/local/bin/uwsgi /etc/uwsgi.ini
}

start_app_celery(){
    celery -A boxing_app worker -l info &
    celery -A boxing_app beat -l info
}

cd /work && clear_cache && install && migrate && deploy && start_app_celery
