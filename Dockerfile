FROM python:3.6-stretch

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /code/
WORKDIR /code/


ENV PYTHONUNBUFFERED 1
RUN python manage.py migrate --settings boxing_app.app_settings

EXPOSE 8000
CMD exec gunicorn boxing_app.wsgi:application --bind 0.0.0.0:8000 --workers 4
