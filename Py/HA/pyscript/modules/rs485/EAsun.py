from pymodbus.client import ModbusSerialClient
from . import entity

IDENTIFIER = "f5ae5fsa8"
DEVICE_NAME = "EPever-XTRA3210N"

Entity = entity.Entity
Entities = (Entity("PV_voltage", "V", "voltage"),
            Entity("PV_current", "A", "current"))


@pyscript_compile
def pull_values(interface, slave):
    try:
        client = ModbusSerialClient(method='rtu',
                                port=interface,
                                baudrate=9600,
                                timeout=5,
                                stopbits=1,
                                bytesize=8,
                                handshaking='N',
                                parity='N',
                                strict=False
                                )
        client.connect()
        result = client.read_holding_registers(address=256, count=2, slave=slave)
        Entities[0].value = result.registers[0]
        Entities[1].value = result.registers[1]
    except Exception:
        Entities[0].value = None
        Entities[1].value = result.registers[1]
    return result