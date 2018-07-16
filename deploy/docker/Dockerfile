FROM python:3-stretch

COPY debain9.sources.list /etc/apt/sources.list
COPY supervisord /etc/init.d/supervisord
COPY supervisord.conf /etc/supervisord.conf

RUN apt-get update && apt-get install -y rcconf python-pip && apt-get clean
RUN pip2 install supervisor==3.3.4 -i https://mirrors.aliyun.com/pypi/simple
RUN mkdir -p /etc/supervisor/
RUN mkdir -p /var/log/supervisor/
RUN rcconf --on supervisord
RUN pip3 install gunicorn==19.8.1 -i https://mirrors.aliyun.com/pypi/simple
RUN apt-get install ffmpeg -y

EXPOSE 8000
