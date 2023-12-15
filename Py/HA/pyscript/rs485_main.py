import json
import paho.mqtt.publish as publish
from rs485 import EPever


@pyscript_compile
def _publish(topic, msg, retain):
    publish.single(topic, payload=msg, qos=1, retain=retain, hostname="core-mosquitto",
                port=1883, client_id="", keepalive=60, will=None,
                auth={"username": "Jarda", "password": "admin"}, tls=None, transport="tcp")


def make_discovery(device_info, name, unit, device_class):
    discovery_prefix = "homeassistant"
    device_name = device_info["name"]
    topic = f"{discovery_prefix}/sensor/{device_name}/{name}/config"
    config = {
            "name": name,
            "state_topic": f"{device_name}/sensor",
            "value_template": "{{ value_json."+name+" }}",
            # "unit_of_measurement": unit,
            "device": device_info,
            "force_update": False,
            "unique_id": name+device_info["identifiers"],
            # "device_class": device_class
            }
    if device_class:
        config["device_class"] = device_class
    if unit:
        config["unit_of_measurement"] = unit
    msg = json.dumps(config)
    return topic, msg


@service
def send_discovery():
    for entity in EPever.modbus_parser.registers.values():
        topic, msg = make_discovery(device_info=EPever.modbus_parser.device_info,
                                    name=entity.name,
                                    unit=entity.unit,
                                    device_class=entity.device_class
                                    )
        task.unique("discovery")
        task.executor(_publish, topic, msg, True)


@service
def loop_over_devices(action=None, id=None):
    task.unique("pull", kill_me=True)
    msg = task.executor(EPever.pull_values, "/dev/ttyUSB0", 1)
    # log.warning(str(msg))
    topic = f"{EPever.DEVICE_NAME}/sensor"
    msg = json.dumps(msg)
    task.unique("publ")
    task.executor(_publish, topic, msg, False)
