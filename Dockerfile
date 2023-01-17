ARG BUILD_FROM
FROM $BUILD_FROM

ENV VERSION=1.0.14-b10


ARG TZ
RUN apk add tzdata git && \
	cp /usr/share/zoneinfo/$TZ /etc/localtime && \
	echo $TZ > /etc/timezone && \
	apk del tzdata

RUN git config --global init.defaultBranch main && \
	git init /openhr20-daemon && \
	cd /openhr20-daemon && \
	git remote add -f origin https://github.com/hannemann/openhr20-daemon.git && \
	git config core.sparseCheckout true && \
	echo "openhr20-daemon/" >> .git/info/sparse-checkout && \
	git pull origin homeassistant_ingress && \
	git status

COPY ./run.sh /run.sh
#RUN chmod +x /run.sh
RUN chmod +x /run.sh && cd /openhr20-daemon/openhr20-daemon && pip install --no-cache-dir -r requirements.txt

CMD [ "/run.sh" ]
