from time import time
import serial
import json
import paho.mqtt.publish as publish


class Juntek:
    def __init__(self, db_table, serial_port):

        self.db_table = db_table
        self.serial_port = serial_port

        self.voltage = 0
        self.current = 0
        self.charged = 0
        self.temperature = 0

        self.read_timestamp = 0
        self.read_data_error = 0
        self.errors = []

    def read_data(self):
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
                station_no, checksum, voltage, current = raw_list[0:4]
                remaining_Ah, cumulative_Ah, energy, runtime = raw_list[4:8]
                temperature, delegate_func, relay_stat = raw_list[8:11]
                current_direction, battery_live, internal_resistance = raw_list[11:14]
                valsum = sum(raw_list[2:14])
            except Exception as e:
                self.errors.append(e)
                self.read_data_error += 1
            else:
                if (valsum % 255) + 1 == checksum:
                    self.voltage = voltage
                    self.current = current if current_direction else -abs(current)
                    self.charged = int(remaining_Ah / 4)
                    self.temperature = temperature - 100
                    self.read_timestamp = time()
                    self.errors = []
                    return True
                else:
                    self.errors.append("Checksum problem")
                    self.read_data_error += 1
        else:
            self.read_data_error += 1
            self.errors.append("No data")

    def write2db(self, conn_obj):
        if (time() - self.read_timestamp) > 10:
            self.errors.append("Data too old.")
            return False

        try:
            with conn_obj.cursor() as cursor:
                cursor.execute(f'''INSERT into public."{self.db_table}"
                    (voltage, current, charged, temperature) 
                    VALUES ({self.voltage}, {self.current}, 
                    {self.charged}, {self.temperature})
                    ''')
        except Exception as e:
            self.errors.append(e)
            return

        return True

    def mqtt_publish(self, ok):

        msg = {"voltage": self.voltage / 100,
               "current": self.current / 100,
               "power": round(self.voltage * self.current / 10000, 1),
               "charged": self.charged / 100,
               "temperature": self.temperature,
               "ok": int(ok)
               }
        msg = json.dumps(msg)

        try:
            publish.single("Juntek", msg, hostname="localhost")
        except Exception as e:
            self.errors.append(e)
            return False
        return True

    def __repr__(self):
        msg = "///////////////////"+"\n"
        if not self.errors:
            msg += f"{'Voltage':<8}{self.voltage / 100:>8} {'V'}\n"
            msg += f"{'Current':<8}{self.current / 100:>8} {'A'}\n"
            msg += f"{'Power':<8}{round(self.voltage * self.current / 10000, 1):>8} {'W'}\n"
            msg += f"{'Charged':<8}{self.charged / 100:>8} {'%'}\n"
            msg += f"{'Temper':<8}{self.temperature:>8} {'°C'}\n"
            msg += f"{'ReadErrors':<8}{self.read_data_error:>8}"
        else:
            for err in self.errors:
                msg += str(err)
                msg += "\n"

        return msg
