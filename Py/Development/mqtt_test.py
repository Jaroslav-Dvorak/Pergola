import paho.mqtt.publish as publish
import json
# publish.single("Juntek", 10, hostname="192.168.167.94")

msg = '{"voltage": 20.45, "current": 1546}'
msg = {"voltage": 20.45, "current": 1546}
msg = json.dumps(msg)

publish.single("Juntek", msg, hostname="192.168.167.94")

# simple(topics, qos=0, msg_count=1, retained=False, hostname="localhost",
#        port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
#        protocol=mqtt.MQTTv311)