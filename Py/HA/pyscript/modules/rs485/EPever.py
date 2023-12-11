from time import sleep
import json
import paho.mqtt.publish as publish
import pymodbus
from . import entity
from random import randint

IDENTIFIER = "f5ae5fsa8"
DEVICE_NAME = "EPever-XTRA3210N"

Entity = entity.Entity
Entities = (Entity("PV_voltage", "V", "voltage"),
            Entity("PV_current", "A", "current"))


@pyscript_compile
def pull_values(interface):
    for entity in Entities:
        entity.value = randint(0, 100)
