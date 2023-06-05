import json
from time import time
# from data_interface import write2db
# import paho.mqtt.publish as publish
# import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
from Grafana.power import Power
from Grafana.bojler import Bojler

power = Power()
bojler = Bojler()

MQTT_TOPIC = [("pico_w/test", 0), ("EAsun", 0), ("EPever", 0)]
client_pub = mqtt.Client()
client_sub = mqtt.Client()


def on_connect(_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client_sub.subscribe(MQTT_TOPIC)


def on_message(_client, userdata, msg):
    try:
        topic = msg.topic
        msg = msg.payload.decode("utf-8")
        msg = json.loads(msg)
        if topic == "pico_w/test":
            power.string_1 = float(msg["power"])
            bojler.string_power = power.string_1
        elif topic == "EPever":
            power.string_2 = int(msg["pv_power"])/100
        elif topic == "EAsun":
            bojler.EAsun_voltage = int(msg["PV_voltage"])/10
    except Exception as e:
        print(e)
        return
    else:
        print(topic+" "+str(msg))



client_sub.on_connect = on_connect
client_sub.on_message = on_message
client_sub.connect("192.168.191.94", 1883, 60)

client_pub.connect("127.0.0.1", 1883, 60)


def job():
    client_pub.publish("grafana/total_power", str(power.power))
    client_pub.publish("grafana/bojler", str(bojler.power))

t1 = time()
client_sub.loop_start()
# schedule.every(1).second.do(job)

while True:
    if (time() - t1) > 1:
        t1 = time()
        job()
    # schedule.run_pending()
    client_pub.loop()

