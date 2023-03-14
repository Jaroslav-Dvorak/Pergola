from time import sleep
from datetime import datetime
import os
import json
import pandas as pd
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import paho.mqtt.publish as publish


class EAsun:
    def __init__(self, db_table, serial_port):
        self.serial_port = serial_port
        self.db_table = db_table
        self.actual_data_parameters = {
            0x100: {
                "battery_level":        True,
                "battery_voltage":      True,
                "battery_current":      False,
                "device_temperature":   False,  # invalid
                "load_dc_voltage":      False,  # invalid
                "load_dc_current":      False,  # invalid
                "load_dc_power":        False,  # invalid
                "PV_voltage":           True,
                "PV_current":           True,
                "PV_power":             True,   # can be computed
                "load_on_off_command":  False,  # invalid, write only
                "battery_charge_state": True,   # 0: off, 1: QC, 2: CV, 3: FlCharge, 6:LiBat activate
            },
            0x216: {
                "inverter_voltage":    True,
                "inverter_current":    True,
                "inverter_frequency":  False,
                "load_current":        True,
                "load_pf":             False,     # invalid
                "load_active_power":   True,
                "load_apparent_power": True,
                "inv_dc_component":    False,    # invalid
                "main_charge_current": True,
                "load_ratio":          True,
                "heatsink_temp_a":     True,
                "heatsink_temp_b":     True,
                "heatsink_temp_c":     True,
                "heatsink_temp_d":     True,      # invalid
                    }
            }

        # self.actual_data_values = {}
        self.errors = []

    def connect(self):
        client = ModbusClient(method='rtu',
                              port=self.serial_port,
                              baudrate=9600,
                              timeout=1,
                              stopbits=1,
                              bytesize=8,
                              handshaking='N',
                              parity='N',
                              strict=False)
        return client

    def read_actual_data(self):
        client = self.connect()
        data = {}
        results = []
        try:
            for addr, item in self.actual_data_parameters.items():
                length = len(item)
                result = client.read_holding_registers(address=addr, count=length, unit=1)
                results.append(result)
                sleep(0.5)
        except TimeoutError:
            return False

        try:
            for result, names in zip(results, self.actual_data_parameters.values()):
                for register, name in zip(result.registers, names):
                    valid = names[name]
                    if valid:
                        data[name] = register
        except AttributeError:
            return False
        else:
            return data
        finally:
            client.close()

    def columns(self):
        columns = []
        for params_valid in self.actual_data_parameters.values():
            for params, valid in params_valid.items():
                if valid:
                    columns.append(params)
        for col in columns:
            print(col)

    def on_off(self, flag):
        client = self.connect()
        client.write_register(0xDF00, int(flag))
        client.close()

    def save_mode(self, enable):
        client = self.connect()
        client.write_register(0xE20C, int(enable))
        client.close()

    def write2db(self, conn_obj, data):
        keys = ", ".join(data.keys())
        values = [str(val) for val in data.values()]
        values = ", ".join(values)
        sqlstr = f'INSERT into public."{self.db_table}" ({keys}) VALUES ({values})'

        try:
            with conn_obj.cursor() as cursor:
                cursor.execute(sqlstr)
        except Exception as e:
            print(e)
            self.errors.append(e)
            return
        else:
            return True

    def mqtt_publish(self, ok, data):

        msg = data.update({"ok": ok})
        msg = json.dumps(msg)

        try:
            publish.single("EAsun", msg, hostname="localhost")
        except Exception as e:
            self.errors.append(e)
            return False
        return True


class OldClassEAsun:
    def __init__(self):
        self.P01_addr = 0x100   # 256
        self.P01 = {  # {"name": [length, db_write, value]
            "battery_level":        [1, True, None],
            "battery_voltage":      [1, True, None],
            "battery_current":      [1, False, None],
            "device_temperature":   [1, False, None],  # invalid
            "load_dc_voltage":      [1, False, None],  # invalid
            "load_dc_current":      [1, False, None],  # invalid
            "load_dc_power":        [1, False, None],  # invalid
            "PV_voltage":           [1, True, None],
            "PV_current":           [1, True, None],
            "PV_power":             [1, True, None],   # can be computed
            "load_on_off_command":  [1, False, None],  # invalid, write only
            "battery_charge_state": [1, True, None],   # 0: off, 1: QC, 2: CV, 3: FlCharge, 6:LiBat activate
            "contr_failure_alarm":  [2, False, None],  # invalid
            "charge_power_total":   [1, False, None]}
        self.P01_length = sum([v[0] for v in self.P01.values()])

        self.P02a_addr = 0x200
        self.P02a = {  # {"name": [length, db_write, value]
             "fault_bits":          [4, True, None],
             "fault_code_1":        [1, True, None],
             "fault_code_2":        [1, True, None],
             "fault_code_3":        [1, True, None],
             "fault_code_4":        [1, True, None],
             "reserved_1":          [4, False, None],    # invalid
             "year_month":          [1, False, None],
             "day_hour":            [1, False, None],
             "min_sec":             [1, False, None],
             "reserved_2":          [1, False, None],    # invalid
             "current_state":       [1, False, None],
             "password_entered":    [1, False, None],
             "bus_voltage":         [1, False, None],
             "grid_voltage":        [1, False, None],
             "grid_current":        [1, False, None],
             "grid_frequency":      [1, False, None]}
        self.P02a_length = sum([v[0] for v in self.P02a.values()])

        self.P02b_addr = 0x216
        self.P02b = {  # {"name": [length, db_write, value]
            "inverter_voltage":    [1, True, None],
            "inverter_current":    [1, True, None],
            "inverter_frequency":  [1, False, None],
            "load_current":        [1, True, None],
            "load_pf":             [1, False, None],     # invalid
            "load_active_power":   [1, True, None],
            "load_apparent_power": [1, True, None],
            "inv_dc_component":    [1, False, None],    # invalid
            "main_charge_current": [1, True, None],
            "load_ratio":          [1, True, None],
            "heatsink_temp_a":     [1, True, None],
            "heatsink_temp_b":     [1, True, None],
            "heatsink_temp_c":     [1, True, None],
            "heatsink_temp_d":     [1, True, None],     # invalid
            "PV_charge_current":   [1, False, None]}
        self.P02b_length = sum([v[0] for v in self.P02b.values()])

        self.P08a_addr = 0xF000
        self.P08a = {    # {"name": [length, db_write, value]
             "power_gen_yesterday":  [1, False, None],
             "power_gen_2_day_bef":  [1, False, None],
             "power_gen_3_day_bef":  [1, False, None],
             "power_gen_4_day_bef":  [1, False, None],
             "power_gen_5_day_bef":  [1, False, None],
             "power_gen_6_day_bef":  [1, False, None],
             "power_gen_7_day_bef":  [1, False, None],
             "charge_lvl_yesterday": [1, False, None],
             "charge_lvl_2_day_bef": [1, False, None],
             "charge_lvl_3_day_bef": [1, False, None],
             "charge_lvl_4_day_bef": [1, False, None],
             "charge_lvl_5_day_bef": [1, False, None],
             "charge_lvl_6_day_bef": [1, False, None],
             "charge_lvl_7_day_bef": [1, False, None],
             "dischg_lvl_yesterday": [1, False, None],
             "dischg_lvl_2_day_bef": [1, False, None],
             "dischg_lvl_3_day_bef": [1, False, None],
             "dischg_lvl_4_day_bef": [1, False, None],
             "dischg_lvl_5_day_bef": [1, False, None],
             "dischg_lvl_6_day_bef": [1, False, None],
             "dischg_lvl_7_day_bef": [1, False, None]}
        self.P08a_length = sum([v[0] for v in self.P08a.values()])

        self.P08b_addr = 0xF015
        self.P08b = {    # {"name": [length, db_write, value]
             "m_chg_lvl_yesterday":  [1, False, None],
             "m_chg_lvl_2_day_bef":  [1, False, None],
             "m_chg_lvl_3_day_bef":  [1, False, None],
             "m_chg_lvl_4_day_bef":  [1, False, None],
             "m_chg_lvl_5_day_bef":  [1, False, None],
             "m_chg_lvl_6_day_bef":  [1, False, None],
             "m_chg_lvl_7_day_bef":  [1, False, None],
             "pwr_consum_yesterday": [1, False, None],
             "pwr_consum_2_day_bef": [1, False, None],
             "pwr_consum_3_day_bef": [1, False, None],
             "pwr_consum_4_day_bef": [1, False, None],
             "pwr_consum_5_day_bef": [1, False, None],
             "pwr_consum_6_day_bef": [1, False, None],
             "pwr_consum_7_day_bef": [1, False, None],
             "pwr_from_m_yesterday": [1, False, None],
             "pwr_from_m_2_day_bef": [1, False, None],
             "pwr_from_m_3_day_bef": [1, False, None],
             "pwr_from_m_4_day_bef": [1, False, None],
             "pwr_from_m_5_day_bef": [1, False, None],
             "pwr_from_m_6_day_bef": [1, False, None],
             "pwr_from_m_7_day_bef": [1, False, None],
             "reserved_1":           [3, False, None]}
        self.P08b_length = sum([v[0] for v in self.P08b.values()])

        self.P08c_addr = 0xF02D
        self.P08c = {  # {"name": [length, db_write, value]
            "battery_charge_today": [1, False, None],
            "battery_dischg_today": [1, False, None],
            "pv_generated_today":   [1, False, None],
            "pwr_consum_today":     [1, False, None],
            "total_running_days":   [1, False, None],
            "count_bat_overdischg": [1, False, None],   # invalid
            "count_bat_full_chg":   [1, False, None],   # invalid
            "bat_charge_total":     [2, False, None],
            "bat_dicharge_total":   [2, False, None],
            "pv_generated_total":   [2, False, None],
            "load_consum_total":    [2, False, None],
            "mains_chg_lvl_today":  [1, False, None],
            "m_pwr_consum_today":   [1, False, None],
            "inverter_work_today":  [1, False, None],
            "bypass_today":         [1, False, None],
            "power_on_time":        [3, False, None],
            "last_equalizing_time": [3, False, None],
            "mains_chg_lvl_total":  [2, False, None],
            "m_pwr_consm_total":    [2, False, None],
            "work_hours_inverter":  [1, False, None],
            "work_hours_bypass":    [1, False, None]}
        self.P08c_length = sum([v[0] for v in self.P08c.values()])

        self.for_write = {}

    def read_data(self):
        client = ModbusClient(method='rtu',
                              port="/dev/ttyUSB1",
                              # port="COM1",
                              baudrate=9600,
                              timeout=5,
                              stopbits=1,
                              bytesize=8,
                              handshaking='N',
                              parity='N',
                              strict=False)
        try:
            result_P01 = client.read_holding_registers(
                address=self.P01_addr, count=self.P01_length, unit=1)
            sleep(0.5)
            result_P02a = client.read_holding_registers(
                address=self.P02a_addr, count=self.P02a_length, unit=1)
            sleep(0.5)
            result_P02b = client.read_holding_registers(
                address=self.P02b_addr, count=self.P02b_length, unit=1)

            sleep(0.5)
            result_P08a = client.read_holding_registers(
                address=self.P08a_addr, count=self.P08a_length, unit=1)
            sleep(0.5)
            result_P08b = client.read_holding_registers(
                address=self.P08b_addr, count=self.P08b_length, unit=1)
            sleep(0.5)
            result_P08c = client.read_holding_registers(
                address=self.P08c_addr, count=self.P08c_length, unit=1)
        except TimeoutError:
            return False

        try:
            for reg, par in zip(result_P01.registers, self.P01):
                self.P01[par][2] = reg
            for reg, par in zip(result_P02a.registers, self.P02a):
                self.P02a[par][2] = reg
            for reg, par in zip(result_P02b.registers, self.P02b):
                self.P02b[par][2] = reg

            for reg, par in zip(result_P08a.registers, self.P08a):
                self.P08a[par][2] = reg
            for reg, par in zip(result_P08b.registers, self.P08b):
                self.P08b[par][2] = reg
            for reg, par in zip(result_P08c.registers, self.P08c):
                self.P08c[par][2] = reg
        except AttributeError:
            return False
        else:
            return True
        finally:
            client.close()

    def on_off(self, flag):
        client = ModbusClient(method='rtu',
                              # port="/dev/ttyUSB1",
                              port="COM1",
                              baudrate=9600,
                              timeout=5,
                              stopbits=1,
                              bytesize=8,
                              handshaking='N',
                              parity='N',
                              strict=False)
        client.write_register(0xDF00, int(flag))
        client.close()

    def save_mode(self, enable):
        client = ModbusClient(method='rtu',
                              # port="/dev/ttyUSB1",
                              port="COM1",
                              baudrate=9600,
                              timeout=5,
                              stopbits=1,
                              bytesize=8,
                              handshaking='N',
                              parity='N',
                              strict=False)
        client.write_register(0xE20C, int(enable))
        client.close()

    def write2db(self):
        pass

    def mqtt_publish(self, ok):
        pass

    def __repr__(self):
        p01 = ""
        for par, val in self.P01.items():
            val = val[2]
            p01 += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        p02a = ""
        for par, val in self.P02a.items():
            val = val[2]
            p02a += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        p02b = ""
        for par, val in self.P02b.items():
            val = val[2]
            p02b += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        p08a = ""
        for par, val in self.P08a.items():
            val = val[2]
            p08a += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        p08b = ""
        for par, val in self.P08b.items():
            val = val[2]
            p08b += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        p08c = ""
        for par, val in self.P08c.items():
            val = val[2]
            p08c += f"{par+':':<21} {str(val)}\n"
            self.for_write[par] = [val]

        return p01 + p02a + p02b + p08a + p08b + p08c

    def to_csv(self):
        self.for_write["time"] = datetime.now().replace(microsecond=0)
        df = pd.DataFrame(self.for_write)
        filename = 'EAsun_data.csv'
        if not os.path.isfile(filename):
            df.to_csv(filename, header=True, index=False, sep=";")
        else:
            df.to_csv(filename, mode='a', header=False, index=False, sep=";")
