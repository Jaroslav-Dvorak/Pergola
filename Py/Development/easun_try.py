from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu',
                      port="/dev/ttyUSB1",
                      baudrate=9600,
                      timeout=5,
                      stopbits=1,
                      bytesize=8,
                      handshaking='N',
                      parity='N',
                      strict=False)

i = 0
while i < 60:
    result = client.read_holding_registers(address=257, count=4, unit=1)
    print(result.registers[0])
    i += 1
    sleep(1)
