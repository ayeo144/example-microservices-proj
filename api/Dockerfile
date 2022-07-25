FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y gcc libpq-dev python-dev git

RUN mkdir /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install git+https://github.com/ayeo144/pika-utils.git

ENTRYPOINT ["tail", "-f", "/dev/null"]