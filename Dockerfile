ARG BUILD_FROM
FROM $BUILD_FROM

ENV VERSION=1.0.15-dev25


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
	git pull origin main && \
	cd /openhr20-daemon/openhr20-daemon && \
	pip install --no-cache-dir -r requirements.txt && \
	cd -

#COPY ./openhr20-daemon /openhr20-daemon/openhr20-daemon
#RUN	cd /openhr20-daemon/openhr20-daemon && \
#	pip install --no-cache-dir -r requirements.txt && \
#	cd -

ARG RUNFILE=run.homeassistant.sh
COPY ./${RUNFILE} /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
