#!/usr/bin/env bash

LOG_PATH="${LOG_PATH:-/var/log/new_boxing}"

build_image(){
    docker build -f ./deploy/docker/Dockerfile -t new_boxing_image deploy/docker
    docker build -f ./deploy/docker/NodeDockerfile -t new_boxing_node_image deploy/docker
}

api(){
    docker run -p 5000:8000 --name new_boxing_app -v `pwd`:/work -v $LOG_PATH:/var/log/new_boxing -v `pwd`/deploy/supervisor:/etc/supervisor -e APP='boxing_app' -d -it new_boxing_image /work/deploy/run.sh
}

console(){
    docker run -p 5001:8000 --name new_boxing_console -v `pwd`:/work -v $LOG_PATH:/var/log/new_boxing -v `pwd`/deploy/supervisor/celery_worker.conf:/etc/supervisor/celery.conf -e APP='boxing_console' -d -it new_boxing_image /work/deploy/run.sh
}

web_console(){
    docker run --name web_console_new_boxing -v `pwd`:/work -d -it new_boxing_node_image /bin/bash /work/deploy/web.sh boxing_console_web
}

web_share(){
    docker run --name web_share_new_boxing -v `pwd`:/work -d -it new_boxing_node_image /bin/bash /work/deploy/web.sh boxing_app_shared_h5
}

filter(){
    echo $(docker ps --filter "name=new_boxing" --all --quiet)
}

filter_web(){
    echo $(docker ps --filter "name=web_" --all --quiet)
}

reset(){
    docker stop $(filter)
    docker rm $(filter)
}

reset_web(){
    docker stop $(filter_web)
    docker rm $(filter_web)
}


restart_api(){
    docker restart $(filter)
}

restart_web(){
    docker restart $(filter_web)
}

init(){
    mkdir -p $LOG_PATH
    if [[ -n $2 ]]; then
        eval $2
    else
        api && console
    fi
}

init_web(){
    if [[ -n $2 ]]; then
        eval $2
    else
        web_console && web_share
    fi
}

deploy(){
    if [ ! "$(filter)" ]; then
        build_image  && init $@
    else
        restart_api
    fi
}

build(){
    if [ ! "$(filter_web)" ]; then
        build_image  && init_web $@
    else
        restart_web
    fi
}

eval $1 $@
