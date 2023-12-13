import json
import paho.mqtt.publish as publish
from rs485 import EPever
from rs485 import EAsun

@pyscript_compile
def _publish(topic, msg, retain):
    publish.single(topic, payload=msg, qos=1, retain=retain, hostname="core-mosquitto",
                port=1883, client_id="", keepalive=60, will=None,
                auth={"username": "Jarda", "password": "admin"}, tls=None, transport="tcp")


def make_discovery(device_name, identifier, name, unit, device_class=None):
    discovery_prefix = "homeassistant"
    topic = f"{discovery_prefix}/sensor/{device_name}/{name}/config" #.encode("utf-8")
    config = {
            "name": name,
            "state_topic": f"{device_name}/sensor",
            "value_template": "{{ value_json."+name+" }}",
            "unit_of_measurement": unit,
            "device": {"identifiers": device_name,
                        "name": device_name,
                        "sw_version": "0.1.0",
                        "model": "HBD-v1",
                        "manufacturer": "JardaDvorak"
                        },
            "force_update": False,
            "unique_id": name+identifier,
            # "device_class": device_class
            }
    if device_class:
        config["device_class"] = device_class
    msg = str(json.dumps(config)) #.encode("utf-8")
    return topic, msg


@service
def send_discovery():
    for entity in EPever.Entities:
        topic, msg = make_discovery(device_name=EPever.DEVICE_NAME,
                                    identifier=EPever.IDENTIFIER,
                                    name=entity.name,
                                    unit=entity.unit,
                                    device_class=entity.device_class
                                    )
        task.unique("discovery")
        task.executor(_publish, topic, msg, True)

@service
def loop_over_devices(action=None, id=None):
    task.unique("pull", kill_me=True)
    res = task.executor(EAsun.pull_values, "/dev/ttyUSB0", 1)
    log.warning(str(res))
    topic = f"{EPever.DEVICE_NAME}/sensor" #.encode("utf-8")
    msg = {}
    for entity in EAsun.Entities:
        msg[entity.name] = entity.value
    msg = json.dumps(msg)
    task.unique("publ")
    task.executor(_publish, topic, msg, False)