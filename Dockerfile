FROM python:3-alpine
RUN apk add tzdata
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG TZ
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apk del tzdata

ENV DEVICES_FILE=./data/devices.db

ENV OPENHR20_MASTER=/dev/ttyUSB0
ENV OPENHR20_BAUD=38400
ENV OPENHR20_TIMEOUT=1

ENV MQTT_HOST=mqtt.example.com
ENV MQTT_PORT=1883
ENV MQTT_QOS=0
ENV MQTT_RETAIN=False
ENV MQTT_STATS_TOPIC=stat/openhr20/RESULT/
ENV MQTT_CMND_TOPIC=cmnd/openhr20/
ENV MQTT_AVAILABILITY_TOPIC=stat/openhr20/AVAILABLE/
ENV MQTT_MODES_RECEIVE='{"auto": "auto", "manu": "manu"}'
ENV MQTT_MODES_PUBLISH='{"auto": "auto", "-": "auto", "manu": "manu"}'
ENV MQTT_PRESETS_RECEIVE='{"antifreeze": "antifreeze", "eco": "eco", "comfort": "comfort", "supercomfort": "supercomfort"}'
ENV MQTT_PRESETS_PUBLISH='{"antifreeze": "antifreeze", "eco": "eco", "comfort": "comfort", "supercomfort": "supercomfort"}'

ENV HTTP_LISTEN_ADDRESS=0.0.0.0
ENV HTTP_PORT=8020
ENV HTTP_DEBUG=False

ENV WS_LISTEN_ADDRESS=0.0.0.0
ENV WS_SCHEME=ws
ENV WS_HOST=0.0.0.0
ENV WS_PORT=8021

CMD [ "python", "./openhr20-daemon.py" ]
