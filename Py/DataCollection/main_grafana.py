import json
from time import time, sleep
from data_interface import read_energy
# import paho.mqtt.publish as publish
# import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
from Grafana.power import Power
from Grafana.bojler import Bojler
from Grafana.energy import Energy

power = Power()
bojler = Bojler()
energy = Energy(read_energy)

MQTT_TOPIC = [("pico_w/test", 0), ("EAsun", 0), ("EPever", 0)]
mqtt_client = mqtt.Client()


def on_connect(_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt_client.subscribe(MQTT_TOPIC)


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


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("127.0.0.1", 1883, 60)


def pub_often():
    mqtt_client.publish("grafana/total_power", str(power.power))
    sleep(0.1)
    mqtt_client.publish("grafana/bojler", str(bojler.power))
    sleep(0.1)

def pub_5min():
    mqtt_client.publish("grafana/energy", json.dumps(energy.get_hours()))
    sleep(0.1)    
    mqtt_client.publish("grafana/text", json.dumps({"DNES VYROBENO": energy.get_day_kwh()}))
    sleep(0.1) 

mqtt_client.loop_start()
# schedule.every(1).second.do(job)
t1 = time()
t2 = time()

while True:
    if (time() - t1) > 2:
        t1 = time()
        try:
            pub_often()
        except Exception as e:
            mqtt_client = mqtt.Client()
            mqtt_client.connect("127.0.0.1", 1883, 60)
            print(e)

    if (time() - t2) > 15:
        t2 = time()
        try:
            pub_5min()
        except Exception as e:
            print(e)
    sleep(0.2)
    # schedule.run_pending()
    # mqtt_client.loop()

