FROM python:3.10.0-alpine3.14

WORKDIR /srv

COPY requirements.txt requirements.txt

RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        python3-dev \
        gcc \
        libffi-dev && \
        pip install -r requirements.txt && \
        apk del \
            python3-dev \
            gcc \
            libressl-dev \
            musl-dev \
            libffi-dev

COPY . .


ENTRYPOINT python bot.py