FROM tarantool/tarantool:3.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    git \
    gcc \
    build-essential

RUN tt rocks install \
    http

WORKDIR /opt/tarantool
COPY ./tarantool .

CMD [ "tarantool", "--config", "/opt/tarantool/config.yml", "/opt/tarantool/dialogs-api.lua" ]
