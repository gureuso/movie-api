FROM python:3.5
MAINTAINER gureuso <wyun13043@gmail.com>

USER root
WORKDIR /root

# bse
RUN apt-get -y update
RUN apt-get -y install python3-pip

# flask
RUN git clone https://github.com/gureuso/movie-api.git
WORKDIR /root/movie-api
RUN pip install virtualenv
RUN virtualenv -p python venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

CMD python manage.py runserver

EXPOSE 5001
