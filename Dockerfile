ARG IMG
FROM ${IMG}

ARG TZ
RUN apk add tzdata && \
	cp /usr/share/zoneinfo/$TZ /etc/localtime && \
	echo $TZ > /etc/timezone && \
	apk del tzdata

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV DEVICES_FILE=./data/devices.db \
	OPENHR20_MASTER=/dev/ttyUSB0 \
	OPENHR20_BAUD=38400 \
	OPENHR20_TIMEOUT=1 \
	MQTT_HOST=mqtt.example.com \
	MQTT_PORT=1883 \
	MQTT_QOS=0 \
	MQTT_RETAIN=False \
	MQTT_STATS_TOPIC=stat/openhr20/RESULT/ \
	MQTT_CMND_TOPIC=cmnd/openhr20/ \
	MQTT_AVAILABILITY_TOPIC=stat/openhr20/AVAILABLE/ \
	MQTT_MODES_RECEIVE='{"auto": "auto", "manu": "manu"}' \
	MQTT_MODES_PUBLISH='{"auto": "auto", "-": "auto", "manu": "manu"}' \
	MQTT_PRESETS_RECEIVE='{"antifreeze": "antifreeze", "eco": "eco", "comfort": "comfort", "supercomfort": "supercomfort"}' \
	MQTT_PRESETS_PUBLISH='{"antifreeze": "antifreeze", "eco": "eco", "comfort": "comfort", "supercomfort": "supercomfort"}' \
	MQTT_DEBUG=False \
	HTTP_LISTEN_ADDRESS=0.0.0.0 \
	HTTP_PORT=8020 \
	HTTP_DEBUG=False \
	WS_LISTEN_ADDRESS=0.0.0.0 \
	WS_SCHEME=ws \
	WS_HOST=0.0.0.0 \
	WS_PORT=8021 \
	WS_DEBUG=False

CMD [ "python", "./openhr20-daemon.py" ]
