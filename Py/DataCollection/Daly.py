import struct
import json
import serial
import paho.mqtt.publish as publish


class Daly:
    def __init__(self, serial_port):
        """code taken from https://github.com/dreadnought/python-daly-bms"""

        self.address = 4
        self.cells_num = 8
        self.serial_port = serial_port

        self.errors = []

    def read_actual_data(self):
        try:
            response_data = self._read("95")
        except Exception as e:
            return False

        if not response_data:
            return False
        cell_voltages = self._split_frames(response_data=response_data, structure=">b 3h x")
        if cell_voltages:
            for cell_num in range(1, self.cells_num+1):
                cell_voltages[f"cell_{cell_num}"] = cell_voltages.pop(cell_num)
        else:
            return False

        cell_voltages_list = list(cell_voltages.values())
        min_voltage = min(cell_voltages_list)
        max_voltage = max(cell_voltages_list)
        difference = max_voltage - min_voltage
        cell_voltages["diff"] = difference
        return cell_voltages

    def mqtt_publish(self, ok, data):
        msg = data
        msg["ok"] = int(ok)
        msg = json.dumps(msg)

        try:
            publish.single("Daly", msg, hostname="localhost")
        except Exception as e:
            print(e)
            self.errors.append(e)
            return False
        return True

    def format_report(self, data):
        for key, val in data.items():
            print(key, val)

    @staticmethod
    def _calc_crc(message_bytes):
        """
        Calculate the checksum of a message
        :param message_bytes: Bytes for which the checksum should get calculated
        :return: Checksum as bytes
        """
        return bytes([sum(message_bytes) & 0xFF])

    def _format_message(self, command, extra=""):
        """
        Takes the command ID and formats a request message
        :param command: Command ID ("90" - "98")
        :return: Request message as bytes
        """
        # 95 -> a58095080000000000000000c2
        message = "a5%i0%s08%s" % (self.address, command, extra)
        message = message.ljust(24, "0")
        message_bytes = bytearray.fromhex(message)
        message_bytes += self._calc_crc(message_bytes)

        return message_bytes

    def _read(self, command):
        """
        Sends a read request to the BMS and reads the response. In case it fails, it retries 'max_responses' times.
        :param command: Command ID ("90" - "98")
        :return: Request message as bytes or False
        """
        ser = serial.Serial(
            port=self.serial_port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
            xonxoff=False,
            writeTimeout=0.5
        )

        if not ser.is_open:
            ser.open()
        message_bytes = self._format_message(command)

        # clear all buffers, in case something is left from a previous command that failed
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        if not ser.write(message_bytes):
            ser.close()
            return False
        max_responses = 3
        x = 0
        response_data = []
        while True:
            b = ser.read(13)
            if len(b) == 0:
                break
            x += 1
            response_crc = self._calc_crc(b[:-1])
            if response_crc != b[-1:]:
                pass
            header = b[0:4].hex()
            if header[4:6] != command:
                continue
            data = b[4:-1]
            response_data.append(data)
            if x == max_responses:
                break

        if response_data:
            ser.close()
            return response_data
        else:
            ser.close()
            return False

    def _split_frames(self, response_data, structure):
        values = {}
        x = 1
        for response_bytes in response_data:
            try:
                parts = struct.unpack(structure, response_bytes)
            except struct.error:
                return False
            if parts[0] != x:
                continue
            for value in parts[1:]:
                values[len(values) + 1] = value
                if len(values) == self.cells_num:
                    return values
            x += 1
