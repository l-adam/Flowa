FROM python:3.8-slim-buster

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt && rm requirements.txt
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
    && chown -R user:user /usr/src/app
USER user

ENV FLASK_ENV development
WORKDIR /usr/src/app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

