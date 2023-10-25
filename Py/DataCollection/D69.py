import paho.mqtt.subscribe as subscribe
from data_interface import write2db
import json

Last_energy = None
zeroing = 516.382   # 1.7.2023

def to_db(msg):
    global Last_energy
    try:
        if (Last_energy is None) or abs(msg["energy"] - Last_energy) < 0.1:
            Last_energy = msg["energy"]
            msg["energy"] += zeroing
            write2db(msg, "D69")
        else:
            print("SMALLER!!!!")
    except Exception as e:
        print(e)


def on_message(client, userdata, message):
    try:
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        to_db(msg)
    except Exception as e:
        print(e)
    else:
        print(msg)


subscribe.callback(on_message, "pico_w/test", hostname="127.0.0.1")
