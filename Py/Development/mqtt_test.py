from time import sleep
import json
from random import randint
import paho.mqtt.publish as publish


def pub(topic):
    voltage = randint(0, 40000)/100
    current = randint(0, 200)/10
    power = round(voltage * current, 2)
    msg = {"voltage": 0.0, "current": 0.0, "power": 0.0, "energy": 224.489}
    msg = json.dumps(msg)

    publish.single(topic, msg, hostname="127.0.0.1")


while True:
    try:
        pub("D69")
        sleep(2)
    except KeyboardInterrupt:
        break
