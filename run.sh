#!/usr/bin/with-contenv bashio


export MQTT_HOST=$(bashio::services mqtt "host")
export MQTT_PORT=$(bashio::services mqtt "port")
export MQTT_USER=$(bashio::services mqtt "username")
export MQTT_PASS=$(bashio::services mqtt "password")

export  OPENHR20_MASTER="$(bashio::config 'OPENHR20_MASTER')"
export  OPENHR20_BAUD="$(bashio::config 'OPENHR20_BAUD')"
export  OPENHR20_TIMEOUT="$(bashio::config 'OPENHR20_TIMEOUT')"
#export  MQTT_HOST="$(bashio::config 'MQTT_HOST')"
#export  MQTT_PORT="$(bashio::config 'MQTT_PORT')"
#export  MQTT_USER="$(bashio::config 'MQTT_USER')"
#export  MQTT_PASS="$(bashio::config 'MQTT_PASS')"
export  MQTT_QOS="$(bashio::config 'MQTT_QOS')"
export  MQTT_RETAIN="$(bashio::config 'MQTT_RETAIN')"
export  MQTT_STATS_TOPIC="$(bashio::config 'MQTT_STATS_TOPIC')"
export  MQTT_CMND_TOPIC="$(bashio::config 'MQTT_CMND_TOPIC')"
export  MQTT_AVAILABILITY_TOPIC="$(bashio::config 'MQTT_AVAILABILITY_TOPIC')"
export  MQTT_PRESETS_PUBLISH="$(bashio::config 'MQTT_PRESETS_PUBLISH')"
export  MQTT_MODES_RECEIVE="$(bashio::config 'MQTT_MODES_RECEIVE')"
export  MQTT_MODES_PUBLISH="$(bashio::config 'MQTT_MODES_PUBLISH')"
export  MQTT_PRESETS_RECEIVE="$(bashio::config 'MQTT_PRESETS_RECEIVE')"
export  MQTT_PRESETS_PUBLISH="$(bashio::config 'MQTT_PRESETS_PUBLISH')"
export  MQTT_DEBUG="$(bashio::config 'MQTT_DEBUG')"
export  HTTP_LISTEN_ADDRESS="$(bashio::config 'HTTP_LISTEN_ADDRESS')"
export  HTTP_PORT="$(bashio::config 'HTTP_PORT')"
export  HTTP_DEBUG="$(bashio::config 'HTTP_DEBUG')"
export  WS_LISTEN_ADDRESS="$(bashio::config 'WS_LISTEN_ADDRESS')"
export  WS_SCHEME="$(bashio::config 'WS_SCHEME')"
export  WS_HOST="$(bashio::config 'WS_HOST')"
export  WS_PORT="$(bashio::config 'WS_PORT')"
export  WS_DEBUG="$(bashio::config 'WS_DEBUG')"
export  TZ="$(bashio::config 'TZ')"

export DEVICES_FILE=/data/devices.db

echo ============ Config ================

RESET_DEVICES="$(bashio::config 'RESET_DEVICES')"
echo $RESET_DEVICES

#DEVICES="$(bashio::config 'DEVICES')"
#echo $DEVICES
#REMOTE_DEVICES="$(bashio::config 'REMOTE_DEVICES')"
#echo $REMOTE_DEVICES
#DEVICE_GROUPS="$(bashio::config 'DEVICE_GROUPS')"
#echo $DEVICE_GROUPS

DEVICE_DB="$(bashio::config 'DEVICE_DB')"

if [ "$RESET_DEVICES" = "true" ]; then
  echo "Writing to $DEVICES_FILE:"
  echo "$DEVICE_DB" > $DEVICES_FILE
#  echo "[names]" > $DEVICES_FILE
#  for i in $DEVICES; do
#    printf "%s = %s\n" ${i%%:*} ${i##*:} >> $DEVICES_FILE
#  done
#  echo "" >> $DEVICES_FILE
#  echo "" >> $DEVICES_FILE
#  echo "[stats]" >> $DEVICES_FILE
#  echo "" >> $DEVICES_FILE
#  echo "[timers]" >> $DEVICES_FILE
#  echo "" >> $DEVICES_FILE
#  echo "[settings]" >> $DEVICES_FILE
#  echo "" >> $DEVICES_FILE
#  echo "[groups]" >> $DEVICES_FILE
#  for i in $DEVICE_GROUPS; do
#    TMP=${i#*:}
#    printf '%s = {"key": "%s", "name": "%s", "devices": [%s]}\n' ${i%%;*} ${TMP%:*} ${TMP#*:} >> $DEVICES_FILE
#  done
#  echo "" >> $DEVICES_FILE
#  echo "[remote_groups]" >> $DEVICES_FILE
#  echo "" >> $DEVICES_FILE
#  echo "[remote_devices]" >> $DEVICES_FILE
#  for i in $REMOTE_DEVICES; do
#    printf "%s = %s\n" ${i%%:*} ${i#*:} >> $DEVICES_FILE
#  done
fi

cat $DEVICES_FILE

#echo $OPENHR20_MASTER
#echo $OPENHR20_BAUD
#echo $OPENHR20_TIMEOUT
#echo $MQTT_HOST
#echo $MQTT_PORT
#echo $MQTT_USER
#echo $MQTT_PASS
#echo $MQTT_QOS
#echo $MQTT_RETAIN
#echo $MQTT_STATS_TOPIC
#echo $MQTT_CMND_TOPIC
#echo $MQTT_AVAILABILITY_TOPIC
#echo $MQTT_PRESETS_PUBLISH
#echo $MQTT_MODES_RECEIVE
#echo $MQTT_MODES_PUBLISH
#echo $MQTT_PRESETS_RECEIVE
#echo $MQTT_PRESETS_PUBLISH
#echo $MQTT_DEBUG
#echo $HTTP_LISTEN_ADDRESS
#echo $HTTP_PORT
#echo $HTTP_DEBUG
#echo $WS_LISTEN_ADDRESS
#echo $WS_SCHEME
#echo $WS_HOST
#echo $WS_PORT
#echo $WS_DEBUG
#echo $TZ
echo ====================================

python /openhr20-daemon/openhr20-daemon.py