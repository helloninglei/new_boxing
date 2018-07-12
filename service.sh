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

reset_api(){
    docker stop $(docker ps --filter "name=new_boxing_" --quiet)
    docker rm $(docker ps --filter "name=new_boxing_" --quiet)
}

reset_web(){
    docker stop $(docker ps --filter "name=web_" --quiet)
    docker rm $(docker ps --filter "name=web_" --filter "status=exited" --filter "status=created"  --quiet)
}


restart_api(){
    docker restart $(docker ps --filter "name=new_boxing_" --quiet)
}

restart_web(){
    docker restart $(docker ps --filter "name=web_" --quiet)
}

deploy(){
    running_container=$(docker ps --filter "name=new_boxing_" --quiet)
    stopped_container=$(docker ps --filter "name=new_boxing_" --filter "status=exited" --filter "status=created" --quiet)
    has_images=$(docker images --filter "reference=new_boxing_*" --quiet)
    if [ "$running_container" ]; then
        for container in $running_container
        do
            docker exec -i $container /bin/bash /work/deploy/run.sh
        done
    elif [ "$stopped_container" ]; then
        docker start ${stopped_container}
    elif [ "$has_images" ]; then
        api && console
    else
        build_image  && init $@
    fi
}

build(){
    running_web=$(docker ps --filter "name=web_" --quiet)
    stopped_web=$(docker ps --filter "name=web_" --filter "status=exited" --filter "status=created"  --quiet)
    web_images=$(docker images --filter "reference=web_*" --quiet)
    if [ "$running_web" ]; then
        for container in $running_web
        do
            docker exec -i $container /bin/bash /work/deploy/run.sh
        done
    elif [ "$stopped_web" ]; then
        docker start $stopped_web
    elif [ "$web_images" ]; then
        web_console && web_share
    else
        build_image  && init_web $@
    fi
}

eval $1 $@
