FROM python:3.6

WORKDIR /srv
ADD requirements.txt /srv/
RUN pip install uwsgi
RUN pip install -r requirements.txt
ADD . /srv/
RUN ./manage.py compilemessages
EXPOSE 8000
