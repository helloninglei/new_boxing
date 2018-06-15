#!/usr/bin/env bash

LOG_PATH='/var/log/new_boxing'

build_image(){
    cd deploy
    docker build -t new_boxing_image .
    docker build -f NodeDockerfile -t new_boxing_node_image .
    cd ..
}

api(){
    docker run -p 5000:8000 --name new_boxing_app -v `pwd`:/work -v $LOG_PATH:/var/log/new_boxing -e APP='boxing_app' -d -it new_boxing_image /work/deploy/run.sh
}

console(){
    docker run -p 5001:8000 --name new_boxing_console -v `pwd`:/work -v $LOG_PATH:/var/log/new_boxing -e APP='boxing_console' -d -it new_boxing_image /work/deploy/run.sh
}

web_console(){
    docker run --name new_boxing_node_console -v `pwd`:/work -d -it new_boxing_node_image /bin/bash /work/deploy/web.sh boxing_console_web
}

web_share(){
    docker run --name new_boxing_node_share -v `pwd`:/work -d -it new_boxing_node_image /bin/bash /work/deploy/web.sh boxing_app_shared_h5
}

filter(){
    echo $(docker ps --filter "name=new_boxing" --all --quiet)
}

filter_node(){
    echo $(docker ps --filter "name=new_boxing_node" --all --quiet)
}

reset(){
    docker stop $(filter)
    docker rm $(filter)
}

restart(){
    docker restart $(filter)
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
        restart
    fi
}

build(){
    if [ ! "$(filter_node)" ]; then
        build_image  && init_web $@
    else
        restart
    fi
}

eval $1 $
