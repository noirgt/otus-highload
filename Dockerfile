FROM alpine:3.19.0


WORKDIR /server
COPY requirements.txt ./requirements.txt

RUN apk --update add \
    python3 \
    py3-requests \
    curl-dev \
    && apk add --update --no-cache --virtual \
    .build-dependencies \
    py3-pip \
    python3-dev \
    build-base \
    && pip3 install --no-cache-dir --break-system-packages --upgrade pip -r requirements.txt \
    && apk del .build-dependencies \
    && rm -rf /var/cache/apk/*

COPY . .
CMD [ "python3", "./app.py" ]
