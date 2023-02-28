from time import sleep
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class EAsun:
    def __init__(self):
        self.P01_addr = 0x100   # 256
        #               {"name": [length, db_write, value]
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
                    "contr_failure_alarm":  [2, False, None],  # invalid
                    "charge_power_total":   [1, False, None]
                    }
        self.P01_length = sum([v[0] for v in self.P01.values()])

        self.P02_addr = 0x200
        #               {"name": [length, db_write, value]
        self.P02 = {"fault_bits":          [4, False, None],
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
                    "grid_frequency":      [1, False, None],
                    "inverter_voltage":    [1, True, None],
                    "inverter_current":    [1, True, None],
                    "inverter_frequency":  [1, True, None],
                    "load_current":        [1, True, None],
                    "load_pf":             [1, True, None],     # invalid
                    "load_active_power":   [1, True, None],
                    "load_apparent_power": [1, True, None],
                    "inv_dc_component":    [1, False, None],    # invalid
                    "main_charge_current": [1, False, None],
                    "load_ratio":          [1, True, None],
                    "heatsink_temp_a":     [1, True, None],
                    "heatsink_temp_b":     [1, True, None],
                    "heatsink_temp_c":     [1, True, None],
                    "heatsink_temp_d":     [1, True, None],     # invalid
                    "PV_charge_current":   [1, True, None]
                    }
        self.P02_length = sum([v[0] for v in self.P02.values()])

        self.P08_addr = 0xF000
        #               {"name": [length, db_write, value]
        self.P08 = {"power_gen_yesterday":  [1, False, None],
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
                    "dischg_lvl_7_day_bef": [1, False, None],
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
                    "reserved_1":           [3, False, None],
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
                    "work_hours_bypass":    [1, False, None],
                    }
        self.P08_length = sum([v[0] for v in self.P08.values()])

    def read_data(self):
        result = client.read_holding_registers(address=257, count=4, unit=1)
            print(result.registers[0])

    def write2db(self):
        pass

    def mqtt_publish(self, ok):
        pass

    def __repr__(self):
        p01 = ""
        for par, val in self.P01.items():
            val = val[2]
            p01 += f"{par+':':<21} {str(val)}\n"

        p02 = ""
        for par, val in self.P02.items():
            val = val[2]
            p02 += f"{par+':':<21} {str(val)}\n"

        return p01 + p02


easun = EAsun()
print(easun)
print(easun.P01_length)
print(easun.P02_length)
print(easun.P08_length)
