from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class EAsun:
    def __init__(self):
        self.P01_addr = 0x100   # 256
        #               {"name": [length, valid, value]
        self.P01 = {"battery_level":        [1, True, None],
                    "battery_voltage":      [1, True, None],
                    "battery_current":      [1, True, None],
                    "device_temperature":   [1, False, None],  # invalid
                    "load_dc_voltage":      [1, False, None],  # invalid
                    "load_dc_current":      [1, False, None],  # invalid
                    "load_dc_power":        [1, False, None],  # invalid
                    "PV_voltage":           [1, True, None],
                    "PV_current":           [1, True, None],
                    "PV_power":             [1, True, None],   # can be computed
                    "load_on_off_command":  [1, False, None],  # invalid, write only
                    "battery_charge_state": [1, True, None],   # 0: off, 1: QC, 2: CV, 3: FlCharge, 6:LiBat activate
                    "charge_power_total":   [1, False, None]
                    }
        self.P01_length = sum([v[0] for v in self.P01.values()])

        # self.battery_level = 0          # 256
        # self.battery_voltage = 0        # 257
        # self.PV_voltage = 0             # 263
        # self.PV_current = 0             # 264
        # self.PV_power = 0               # 265
        # self.battery_chargestate = 0    # 267
        # self.charge_power = 0           # 270    (count = 14)

        self.inverter_operation = 0     # 528
        self.inverter_current = 0       # 537
        self.inverter_power = 0         # 539
        self.main_charge_current = 0    # 542
        self.load_ratio = 0             # 543
        self.DCDC_temp = 0              # 544
        self.DCAC_temp = 0              # 545
        self.translator_temp = 0        # 546
        self.PV_charge_current = 0      # 548   (count = 20)

        self.battery_charge_daily = 0   # 61485 ??
        self.load_daily_consumption = 0   # 61485 ??
        self.battery_discharge_daily = 0  # 61486
        self.PV_daily_comsuption = 0    # 61487 ??
        self.PV_daily_consumption = 0   # 61487 ??
        self.inverter_uptime = 0        # 61489
        self.inverter_PV_generated = 0  # 61496
        self.main_load_power_daily = 0  # 61501
        self.last_equalization = 0      # 61507



        # result = client.read_holding_registers(address=256, count=16, unit=1)
        # for addr, val in enumerate(result.registers, 256):
        #     print(addr, val)
        # result = client.read_holding_registers(address=528, count=22, unit=1)
        # for addr, val in enumerate(result.registers, 528):
        #     print(addr, val)
        #
        # result = client.read_holding_registers(address=61485, count=25, unit=1)
        # for addr, val in enumerate(result.registers, 61485):
        #     print(addr, val)


    def write2db(self):
        pass

    def mqtt_publish(self, ok):
        pass

    def __repr__(self):
        pass


easun = EAsun()
# easun.read_data('/dev/ttyUSB1')

