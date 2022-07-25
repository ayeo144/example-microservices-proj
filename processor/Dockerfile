FROM python:3.8-slim

RUN apt-get -y update
RUN apt-get -y install git

RUN mkdir /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install git+https://github.com/ayeo144/pika-utils.git

ENTRYPOINT ["tail", "-f", "/dev/null"]