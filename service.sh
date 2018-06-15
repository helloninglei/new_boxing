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

api(){
    docker run -p 5000:8000 --name new_boxing_app -v $PROJECT_PATH:/work -v $LOG_PATH:/var/log/boxing -e APP='boxing_app' -d -it new_boxing_image /bin/bash /work/deploy/run.sh
}

console(){
    docker run -p 5001:8000 --name new_boxing_console -v $PROJECT_PATH:/work -v $LOG_PATH:/var/log/boxing -e APP='boxing_console' -d -it new_boxing_image /bin/bash /work/deploy/run.sh
}

filter(){
    echo $(docker ps --filter "name=new_boxing" --all --quiet)
}

reset(){
    docker stop $(filter)
    docker rm $(filter)
}


restart(){
    docker restart $(filter)
}

init(){
    if [ -z $2 ]; then
        eval $2
    else
        api && console
    fi
}

deploy(){
    if [ ! "$(filter)" ]; then
        build  && init
    else
        restart
    fi
}

eval $1
