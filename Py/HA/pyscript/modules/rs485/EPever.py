from pymodbus.client import ModbusSerialClient
from pymodbus.constants import Endian
from . import modbus

modbus_parser = modbus.ModbusParser(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
modbus_parser.device_info["identifiers"] = "f5ae5fsa8"
modbus_parser.device_info["name"] = "MPPT-100V"
modbus_parser.device_info["sw_version"] = "V1.1"
modbus_parser.device_info["model"] = "XTRA3210N"
modbus_parser.device_info["manufacturer"] = "EPever"

modbus_parser.add_address_range(start=0x3000, end=0x3008)
modbus_parser.add_register(address=0x3000, name="PV_array_rated_voltage", unit="V", device_class="voltage", datatype="uint16", gain=0.01)
modbus_parser.add_register(0x3001,              "PV_array_rated_current",      "A",              "current",          "uint16",      0.01)
modbus_parser.add_register((0x3002, 0x3003),    "PV_array_rated_power",        "W",              "power",            "uint32",      0.01)
modbus_parser.add_register(0x3004,              "Battery_voltage",             "V",              "voltage",          "uint16",      0.01)
modbus_parser.add_register(0x3005,              "Rated_chaging_current",       "A",              "current",          "uint16",      0.01)
modbus_parser.add_register((0x3006, 0x3007),    "Rated_chaging_power",         "W",              "power",            "uint32",      0.01)
modbus_parser.add_register(0x3008,              "Charging_mode",               None,             None,               "uint16",      1)
modbus_parser.add_address_range(start=0x300E, end=0x300E)
modbus_parser.add_register(0x300E,              "PV_output_current_of_load",   "A",              "current",          "uint16",      0.01)

modbus_parser.add_address_range(start=0x3100, end=0x3112)
modbus_parser.add_register(0x3100,              "PV_array_voltage",            "V",              "voltage",          "uint16",      0.01)
modbus_parser.add_register(0x3101,              "PV_array_current",            "A",              "current",          "uint16",      0.01)
modbus_parser.add_register((0x3102, 0x3103),    "PV_array_voltage",            "W",              "power",            "uint32",      0.01)
modbus_parser.add_register(0x3104,              "Battery_voltage",             "V",              "voltage",          "uint16",      0.01)
modbus_parser.add_register(0x3105,              "Battery_charging_current",    "A",              "current",          "uint16",      0.01)
modbus_parser.add_register((0x3106, 0x3107),    "Battery_charging_power",      "W",              "power",            "uint32",      0.01)
modbus_parser.add_register(0x310C,              "Load_voltage",                "V",              "voltage",          "uint16",      0.01)
modbus_parser.add_register(0x310D,              "Load_current",                "A",              "current",          "uint16",      0.01)
modbus_parser.add_register((0x310E, 0x310E),    "Load_power",                  "W",              "power",            "uint32",      0.01)
modbus_parser.add_register(0x3110,              "Battery_temperature",         "°C",             "temperature",      "uint16",      0.01)
modbus_parser.add_register(0x3111,              "Temperature_inside_case",     "°C",             "temperature",      "uint16",      0.01)
modbus_parser.add_register(0x3112,              "Heatsink_temperature",        "°C",             "temperature",      "uint16",      0.01)
modbus_parser.add_address_range(start=0x311A, end=0x311B)
modbus_parser.add_register(0x311A,              "Battery_SOC",                 "%",              "battery",          "uint16",      0.01)
modbus_parser.add_register(0x311B,              "Remote_battery_temperature",  "°C",             "temperature",      "uint16",      0.01)
modbus_parser.add_address_range(start=0x311D, end=0x311D)
modbus_parser.add_register(0x311D,              "Battery_real_rated_power",    "V",              "voltage",          "uint16",      0.01)

modbus_parser.add_address_range(start=0x3200, end=0x3201)
modbus_parser.add_register(0x3200,              "Battery_status",              None,             None,               "uint16",      1)
modbus_parser.add_register(0x3201,              "Charging_equipment_status",   None,             None,               "uint16",      1)

modbus_parser.add_address_range(start=0x3300, end=0x331E)
modbus_parser.add_register((0x3300, 0x3301),    "Maximum_PV_voltage_today",    "V",              "voltage",          "uint32",      0.01)
modbus_parser.add_register((0x3302, 0x3303),    "Maximum_battery_voltage_today", "V",            "voltage",          "uint32",      0.01)
modbus_parser.add_register((0x3304, 0x3305),    "Consumed_energy_today",       "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x3306, 0x3307),    "Consumed_energy_this_month",  "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x3308, 0x3309),    "Consumed_energy_this_year",   "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x330A, 0x330B),    "Total_consumed_energy",       "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x330C, 0x330D),    "Generated_energy_today",      "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x330E, 0x330F),    "Generated_energy_this_month", "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x3310, 0x3311),    "Generated_energy_this_year",  "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x3312, 0x3313),    "Total_generated_energy",      "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x3314, 0x3315),    "Carbon_dioxide_reduction",    "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register((0x331B, 0x331C),    "Battery_current",             "kWh",            "energy",           "uint32",      0.01)
modbus_parser.add_register(0x331D,              "Battery_temperature",         "°C",             "temperature",      "uint16",      0.01)
modbus_parser.add_register(0x331E,              "Ambient_temperature",         "°C",             "temperature",      "uint16",      0.01)


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
        modbus_parser.merge_data_into_registers(addr_obj, reg_data)

        break

    return modbus_parser.get_all_values()
