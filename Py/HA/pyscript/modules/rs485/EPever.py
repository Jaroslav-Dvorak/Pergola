from pymodbus.client import ModbusSerialClient
from pymodbus.constants import Endian
from . import modbus

IDENTIFIER = "f5ae5fsa8"
DEVICE_NAME = "EPever-XTRA3210N"

reg_data = [10000, 3000, 12464, 1, 2400, 3000, 12464, 1, 2]

modbus_parser = modbus.ModbusParser(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
modbus_parser.add_address_range(start=0x3000, end=0x3008)
modbus_parser.add_register(address=0x3000, name="PV array rated voltage", unit="V", device_class="voltage",
                           datatype="uint16", gain=0.01)
modbus_parser.add_register(0x3001, "PV array rated current", "A", "current", "uint16", 0.01)
modbus_parser.add_register((0x3002, 0x3003), "PV array rated power", "W", "power", "uint32", 0.01)
modbus_parser.add_register(0x3004, "Battery voltage", "V", "voltage", "uint16", 0.01)
modbus_parser.add_register(0x3005, "Rated chaging current", "A", "current", "uint16", 0.01)
modbus_parser.add_register((0x3006, 0x3007), "Rated chaging power", "W", "current", "uint32", 0.01)
modbus_parser.add_register(0x3008, "Charging mode", None, None, "uint16", 1)


# for addr_obj in modbus_parser.address_ranges:
#     start_address = addr_obj.start
#     count = addr_obj.count
#     # result = client.read_input_registers(address=start_address, count=count, slave=slave)
#     # reg_data = result.registers
#     reg_data = [10000, 3000, 12464, 1, 2400, 3000, 12464, 1, 2]
#
#     for addr, data in zip(addr_obj.range, reg_data):
#         modbus_parser.registers[addr].register_values.append(data)
# #         print(hex(addr), data)


@pyscript_compile
def pull_values(interface, slave):
    # try:
    #     client = ModbusSerialClient(method='rtu',
    #                                 port=interface,
    #                                 baudrate=115200,
    #                                 timeout=5,
    #                                 stopbits=1,
    #                                 bytesize=8,
    #                                 handshaking='N',
    #                                 parity='N',
    #                                 strict=False)
    #     client.connect()
    #     result = client.read_input_registers(address=0x3100, count=8, slave=slave)
    #     Entities[0].value = result.registers[0]
    #     Entities[1].value = result.registers[1]
    #     client.close()
    # except Exception as e:
    #     return False
    # else:
    #     return True

    for addr_obj in modbus_parser.address_ranges:
        start_address = addr_obj.start
        count = addr_obj.count
        # result = client.read_input_registers(address=start_address, count=count, slave=slave)
        # reg_data = result.registers
        reg_data = [10000, 3000, 12464, 1, 2400, 3000, 12464, 1, 2]

        for addr, data in zip(addr_obj.range, reg_data):
            modbus_parser.registers[addr].register_values.append(data)

    return modbus_parser.get_all_values()

