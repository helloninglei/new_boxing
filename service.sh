#!/usr/bin/env bash

# 管理docker容器

pull(){
    git pull origin master
}

init(){
    docker run -p 8001:8000 --name new_boxing_app -v /new_boxing:/work -v /new_boxing/boxing_app/uwsgi.ini:/etc/uwsgi.ini -v /var/log/boxing:/var/log/boxing -d -it new_boxing_image /bin/bash /work/run.sh
    docker run -p 8002:8000 --name new_boxing_console -v /new_boxing:/work -v /new_boxing/boxing_console/uwsgi.ini:/etc/uwsgi.ini -v /var/log/boxing:/var/log/boxing -d -it new_boxing_image /bin/bash /work/run.sh
}

reset(){
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
}

start(){
    docker start new_boxing_app
    docker start new_boxing_console
}

stop(){
    docker stop new_boxing_app
    docker stop new_boxing_console
}

restart(){
    docker restart new_boxing_app
    docker restart new_boxing_console
}

eval $1
