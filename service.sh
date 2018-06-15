#!/usr/bin/env bash

PROJECT_PATH="${RUN_PATH:-/workspace/new_boxing}"
LOG_PATH=$PROJECT_PATH'/logs'

build(){
    cd deploy
    sh ./build.sh
}

pull(){
    git pull origin master
}

init(){
    build
    docker run -p 5000:8000 --name new_boxing_app -v $PROJECT_PATH:/work -v $LOG_PATH:/var/log/boxing -e APP='boxing_app' -d -it new_boxing_image /bin/bash /work/deploy/run.sh
    docker run -p 5001:8000 --name new_boxing_console -v $PROJECT_PATH:/work -v $LOG_PATH:/var/log/boxing -e APP='boxing_console' -d -it new_boxing_image /bin/bash /work/deploy/run.sh
}

reset(){
    docker stop $(docker ps --filter "name=new_boxing" --all --quiet)
    docker rm $(docker ps --filter "name=new_boxing" --all --quiet)
}

start(){
    docker start $(docker ps --filter "name=new_boxing" --all --quiet)
}

stop(){
    docker stop $(docker ps --filter "name=new_boxing" --all --quiet)
}

restart(){
    docker restart $(docker ps --filter "name=new_boxing" --all --quiet)
}


deploy(){
    pull && restart
}
eval $1
