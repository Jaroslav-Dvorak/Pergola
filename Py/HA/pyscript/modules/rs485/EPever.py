import paho.mqtt.publish as publish
import pymodbus
from time import sleep


@pyscript_compile
def publ(arg):
    publish.single("zdtestjakpes/konokun", payload="{'čuně': 555}", qos=0, retain=False, hostname="core-mosquitto",
        port=1883, client_id="", keepalive=60, will=None,
        auth={"username":"Jarda", "password":"admin"}, tls=None, transport="tcp")
    sleep(2)

