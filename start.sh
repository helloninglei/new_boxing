#!/usr/bin/env bash
docker run -d -p 8001:8000 --name new_boxing_app -v .:/work boxing_app/uwsgi.ini:/etc/uwsgi.ini /bin/bash -it new_boxing_image /work/run.sh
docker run -d -p 8002:8000 --name new_boxing_console -v .:/work boxing_console:/etc/uwsgi.ini -it new_boxing_image /bin/bash /work/run.sh
