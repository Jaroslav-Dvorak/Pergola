import serial
import json
import paho.mqtt.publish as publish


class Juntek:
    def __init__(self, db_table, serial_port):

        self.db_table = db_table
        self.serial_port = serial_port

        self.data_idx_names = [
            "station_no",
            "checksum",
            "voltage",
            "current",
            "remaining_Ah",
            "cumulative_Ah",
            "energy",
            "runtime",
            "temperature",
            "delegate_func",
            "relay_stat",
            "current_direction",
            "battery_live",
            "internal_resistance"
                                    ]
        self.read_data_error = 0
        self.errors = []

    def read_actual_data(self):
        try:
            with serial.Serial(self.serial_port, 115200, timeout=1, write_timeout=1) as ser:
                ser.write(b':R50=1,2,1,\r\n')
                line = ser.readline()
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            self.errors.append(e)
            self.read_data_error += 1
            return

        if line:
            try:
                line = line.decode("utf-8")
                raw = line.split("=")[1]
                raw_list = raw.split(",")
                raw_list = [int(val) for val in raw_list[0:14]]
                data = {}
                ret_data = {}
                for idx, name in enumerate(self.data_idx_names):
                    data[name] = raw_list[idx]
                valsum = sum(raw_list[2:14])
            except Exception as e:
                self.errors.append(e)
                self.read_data_error += 1
            else:
                if (valsum % 255) + 1 == data["checksum"]:
                    ret_data["voltage"] = data["voltage"]
                    if data["current_direction"]:
                        ret_data["current"] = data["current"]
                    else:
                        ret_data["current"] = -abs(data["current"])
                    ret_data["charged"] = int(data["remaining_Ah"] / 4)
                    ret_data["temperature"] = data["temperature"] - 100
                    self.errors = []
                    return ret_data
                else:
                    self.errors.append("Checksum problem")
                    self.read_data_error += 1
        else:
            self.read_data_error += 1
            self.errors.append("No data")

    def write2db(self, conn_obj, data):
        cols = list(data.keys())
        cols = ",".join(cols)
        vals = list(data.values())
        vals = [str(val) for val in vals]
        vals = ",".join(vals)
        try:
            with conn_obj.cursor() as cursor:
                cursor.execute(f'INSERT into public."{self.db_table}" ({cols}) VALUES ({vals})')
        except Exception as e:
            self.errors.append(e)
            return False
        else:
            return True

    def mqtt_publish(self, ok, data):
        voltage = data["voltage"] / 100
        current = data["current"] / 100
        power = round(voltage * current, 1)
        charged = data["charged"] / 100
        temperature = data["temperature"]
        ok = int(ok)

        msg = {"voltage": voltage,
               "current": current,
               "power": power,
               "charged": charged,
               "temperature": temperature,
               "ok": ok
               }
        msg = json.dumps(msg)

        try:
            publish.single("Juntek", msg, hostname="localhost")
        except Exception as e:
            self.errors.append(e)
            return False
        return True

    def format_report(self, data):
        voltage = data["voltage"] / 100
        current = data["current"] / 100
        power = round(voltage * current, 1)
        charged = data["charged"] / 100
        temperature = data["temperature"]

        msg = "///////////////////"+"\n"
        if not self.errors:
            msg += f"{'Voltage':<8}{voltage:>8} {'V'}\n"
            msg += f"{'Current':<8}{current:>8} {'A'}\n"
            msg += f"{'Power':<8}{power:>8} {'W'}\n"
            msg += f"{'Charged':<8}{charged:>8} {'%'}\n"
            msg += f"{'Temper':<8}{temperature:>8} {'°C'}\n"
            msg += f"{'ReadErrors':<8}{self.read_data_error:>8}"
        else:
            for err in self.errors:
                msg += str(err)
                msg += "\n"

        return msg
