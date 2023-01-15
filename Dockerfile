ARG BUILD_FROM
FROM $BUILD_FROM


ARG TZ
RUN apk add tzdata && \
	cp /usr/share/zoneinfo/$TZ /etc/localtime && \
	echo $TZ > /etc/timezone && \
	apk del tzdata

COPY ./openhr20-daemon /openhr20-daemon
COPY ./run.sh /run.sh
#RUN chmod +x /run.sh
RUN chmod +x /run.sh && cd /openhr20-daemon && pip install --no-cache-dir -r requirements.txt

#CMD [ "python", "./openhr20-daemon.py" ]
CMD [ "/run.sh" ]
