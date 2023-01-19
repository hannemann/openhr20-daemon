#!/usr/bin/with-contenv bashio

export MQTT_HOST=$(bashio::services mqtt "host")
export MQTT_PORT=$(bashio::services mqtt "port")
export MQTT_USER=$(bashio::services mqtt "username")
export MQTT_PASS=$(bashio::services mqtt "password")

export OPENHR20_MASTER="$(bashio::config 'OPENHR20_MASTER')"
export OPENHR20_BAUD="$(bashio::config 'OPENHR20_BAUD')"
export OPENHR20_TIMEOUT="$(bashio::config 'OPENHR20_TIMEOUT')"
export OPENHR20_DEBUG="$(bashio::config 'OPENHR20_DEBUG')"
export MQTT_QOS="$(bashio::config 'MQTT_QOS')"
export MQTT_RETAIN="$(bashio::config 'MQTT_RETAIN')"
export MQTT_STATS_TOPIC="$(bashio::config 'MQTT_STATS_TOPIC')"
export MQTT_CMND_TOPIC="$(bashio::config 'MQTT_CMND_TOPIC')"
export MQTT_AVAILABILITY_TOPIC="$(bashio::config 'MQTT_AVAILABILITY_TOPIC')"
export MQTT_MODES_RECEIVE="$(bashio::config 'MQTT_MODES_RECEIVE')"
export MQTT_MODES_PUBLISH="$(bashio::config 'MQTT_MODES_PUBLISH')"
export MQTT_PRESETS_RECEIVE="$(bashio::config 'MQTT_PRESETS_RECEIVE')"
export MQTT_PRESETS_PUBLISH="$(bashio::config 'MQTT_PRESETS_PUBLISH')"
export MQTT_DEBUG="$(bashio::config 'MQTT_DEBUG')"
export HTTP_LISTEN_ADDRESS="$(bashio::config 'HTTP_LISTEN_ADDRESS')"
export HTTP_PORT="$(bashio::config 'HTTP_PORT')"
export HTTP_DEBUG="$(bashio::config 'HTTP_DEBUG')"
export WS_LISTEN_ADDRESS="$(bashio::config 'WS_LISTEN_ADDRESS')"
export WS_SCHEME="$(bashio::config 'WS_SCHEME')"
export WS_HOST="$(bashio::config 'WS_HOST')"
export WS_PORT="$(bashio::config 'WS_PORT')"
export WS_DEBUG="$(bashio::config 'WS_DEBUG')"
export TZ="$(bashio::config 'TZ')"

export DEVICES_FILE=/data/devices.db

export BASE_URL=$(bashio::addon.ingress_url)

RESET_DEVICES="$(bashio::config 'RESET_DEVICES')"
DEVICE_DB="$(bashio::config 'DEVICE_DB')"

if [ "$RESET_DEVICES" = "true" ]; then
  echo "Writing to $DEVICES_FILE:"
  echo "$DEVICE_DB" > $DEVICES_FILE
fi

echo ============ Devices DB ================
cat $DEVICES_FILE
echo ============ OpenHR20 ================
bashio::log.info $OPENHR20_MASTER
echo ====================================

python /openhr20-daemon/openhr20-daemon/openhr20-daemon.py