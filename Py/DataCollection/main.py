import subprocess
from time import sleep, time
from data_interface import write2db, conn
from Juntek import Juntek
from EAsun import EAsun
from Daly import Daly
from EPever import EPever

subprocess.run(["lxterminal", "-e", "python3 D69.py"])


juntek = Juntek(serial_port='/dev/ttyUSB0')
easun = EAsun(serial_port='/dev/ttyUSB0')
daly = Daly(serial_port='/dev/ttyUSB0')
epever = EPever(serial_port='/dev/ttyUSB0')


def wait():
    try:
        sleep(0.5)
    except KeyboardInterrupt:
        return False
    else:
        return True


if __name__ == '__main__':
    while True:

        ok = False
        juntek_data = juntek.read_actual_data()
        if juntek_data:
            if write2db(data=juntek_data, db_table="Juntek"):
                ok = True
            juntek.mqtt_publish(ok=ok, data=juntek_data)
            print(juntek.format_report(juntek_data))

        if not wait():
            break

        ok = False
        EAsun_data = easun.read_actual_data()
        if EAsun_data:
            if write2db(data=EAsun_data, db_table="EAsun"):
                ok = True
            easun.mqtt_publish(ok=ok, data=EAsun_data)
            for par, val in EAsun_data.items():
                print(f"{par+':':<21} {str(val)}")

        if not wait():
            break

        ok = False
        epever_data = epever.read_actual_data()
        if epever_data:
            if write2db(data=epever_data, db_table="EPever"):
                ok = True
            epever.mqtt_publish(ok=ok, data=epever_data)
            # print(epever.format_report(daly_data))
            for k, v in epever_data.items():
                print(k, v)

        if not wait():
            break

        ok = False
        daly_data = daly.read_actual_data()
        if daly_data:
            if write2db(data=daly_data, db_table="Daly"):
                ok = True
            daly.mqtt_publish(ok=ok, data=daly_data)
            print(daly.format_report(daly_data))

        if not wait():
            break

        if juntek_data and EAsun_data:
            try:
                if EAsun_data["PV_voltage"] > 3000:
                    easun.sun_avaible = True
                elif EAsun_data["PV_voltage"] < 1200:
                    easun.sun_avaible = False

                if juntek_data["charged"] < 2000 and not easun.sun_avaible and easun.last_start < time()-7200:
                    if easun.inverter_run is None or easun.inverter_run is True:
                        easun.on_off(False)
                        easun.inverter_run = False
                else:
                    if easun.inverter_run is None or easun.inverter_run is False:
                        easun.last_start = time()
                        easun.on_off(True)
                        easun.inverter_run = True
            except Exception as e:
                print(e)

conn.close()
