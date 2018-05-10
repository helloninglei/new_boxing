#!/usr/bin/env bash
docker run -p 8001:8000 --name new_boxing_app -v /new_boxing:/work -v /new_boxing/boxing_app/uwsgi.ini:/etc/uwsgi.ini -v /var/log/boxing:/var/log/boxing -d -it new_boxing_image /bin/bash /work/run.sh
docker run -p 8002:8000 --name new_boxing_console -v /new_boxing:/work -v /new_boxing/boxing_console/uwsgi.ini:/etc/uwsgi.ini -v /var/log/boxing:/var/log/boxing -d -it new_boxing_image /bin/bash /work/run.sh
