FROM python:3.6-stretch

RUN pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN useradd work
RUN chown -R work /work
USER work

EXPOSE 8000
