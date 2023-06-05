import paho.mqtt.subscribe as subscribe
from data_interface import write2db
import json


def on_message(client, userdata, message):
    try:
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        write2db(msg, "D69")
    except Exception as e:
        print(e)
    else:
        print(msg)


subscribe.callback(on_message, "pico_w/test", hostname="127.0.0.1")
