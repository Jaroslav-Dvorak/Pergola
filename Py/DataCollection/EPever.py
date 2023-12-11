from datetime import datetime
import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import paho.mqtt.publish as publish


class EPever:
    """https://github.com/tekk/Tracer-RS485-Modbus-Blynk-V2/blob/master/doc/1733_modbus_protocol.pdf"""
    def __init__(self, serial_port):
        self.serial_port = serial_port

        self.errors = []
        self.read_data_error = 0

    def connect(self):
        try:
            client = ModbusClient(method='rtu',
                                  port=self.serial_port,
                                  baudrate=115200,
                                  timeout=5,
                                  stopbits=1,
                                  bytesize=8,
                                  handshaking='N',
                                  parity='N',
                                  strict=False)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            self.errors.append(e)
            self.read_data_error += 1
            return False
        else:
            return client

    def read_actual_data(self):
        client = self.connect()
        if not client:
            return False

        data = {}
        unit = 1
        try:
            result = client.read_input_registers(address=0x3100, count=8, unit=unit)
            data["pv_voltage"] = result.registers[0]
            data["pv_current"] = result.registers[1]
            data["pv_power"] = self.merge_ints(result.registers[2], result.registers[3])
            data["battery_voltage"] = result.registers[4]
            # mppt_data["Battery_current"] = result.registers[5]
            data["battery_power"] = self.merge_ints(result.registers[6], result.registers[7])

            result = client.read_input_registers(address=0x310C, count=7, unit=unit)
            data["load_current"] = result.registers[1]
            data["load_power"] = self.merge_ints(result.registers[2], result.registers[3])
            # mppt_data["device_temperature"] = result.registers[5]
            data["heatsink_temperature"] = result.registers[6]

            result = client.read_input_registers(address=0x311B, count=1, unit=unit)
            data["battery_temperature"] = result.registers[0]

            # result = client.read_input_registers(address=0x3304, count=2, unit=unit)
            # mppt_data["consumed_energy_today"] = merge_ints(result.registers[0], result.registers[1])
            #
            # result = client.read_input_registers(address=0x330A, count=4, unit=unit)
            # mppt_data["total_consumed_energy"] = merge_ints(result.registers[0], result.registers[1])
            # mppt_data["generated_energy_today"] = merge_ints(result.registers[2], result.registers[3])
            #
            # result = client.read_input_registers(address=0x3312, count=4, unit=unit)
            # mppt_data["total_generated_energy"] = merge_ints(result.registers[0], result.registers[1])
            # mppt_data["carbon_dioxide_reduction"] = merge_ints(result.registers[2], result.registers[3])

            result = client.read_input_registers(address=0x331B, count=2, unit=unit)
            data["Battery_current"] = self.uint2int(self.merge_ints(result.registers[0], result.registers[1]))

            result = client.read_input_registers(address=0x3200, count=2, unit=unit)
            data["battery_status"] = result.registers[0]
            data["charging_status"] = result.registers[1]
        except TimeoutError:
            return False
        except AttributeError:
            return False
        else:
            return data
        finally:
            client.close()

    def read_time(self, unit):
        with self.connect() as client:
            result = client.read_holding_registers(address=0x9013, count=3, unit=unit)
            second, minute = self.split_16bit_to_8bit(result.registers[0])
            hour, day = self.split_16bit_to_8bit(result.registers[1])
            month, year = self.split_16bit_to_8bit(result.registers[2])
            year += 2000
            print("čas: " + str(hour) + ":" + str(minute) + ":" + str(second))
            print("datum:" + str(day) + "." + str(month) + "." + str(year))
            return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def write_time(self, dt, unit):
        registers = [
            self.merge_8bit_to_16bit(dt.second, dt.minute),
            self.merge_8bit_to_16bit(dt.hour, dt.day),
            self.merge_8bit_to_16bit(dt.month, dt.year - 2000)
        ]

        with self.connect() as client:
            client.write_registers(address=0x9013, values=registers, unit=unit)

    def charging_on_off(self, value):
        with self.connect() as client:
            client.write_coil(address=0, value=int(value), unit=0)

    @staticmethod
    def uint2int(uint):
        if uint > 2147483647:
            return uint - 4294967295
        else:
            return uint

    @staticmethod
    def merge_ints(low, high):
        res = (high << 16) | low
        return res

    @staticmethod
    def split_16bit_to_8bit(x):
        high = (x >> 8) & 0xff
        low = x & 0xff
        return low, high

    @staticmethod
    def merge_8bit_to_16bit(low, high):
        res = (high << 8) | low
        return res

    def mqtt_publish(self, ok, data):
        msg = data
        msg["ok"] = int(ok)
        msg = json.dumps(msg)

        try:
            publish.single("EPever", msg, hostname="localhost")
        except Exception as e:
            print(e)
            self.errors.append(e)
            return False
        return True
