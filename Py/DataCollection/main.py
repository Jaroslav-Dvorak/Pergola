from time import sleep
import json
import psycopg2
from Juntek import Juntek
from EAsun import EAsun
from Daly import Daly


with open("../db_conf.json", "r") as f:
    raw = f.read()
    conn_params = json.loads(raw)

conn = psycopg2.connect(**conn_params)
conn.set_session(autocommit=True)

juntek = Juntek(db_table="Juntek", serial_port='/dev/ttyUSB0')
easun = EAsun(db_table="EAsun", serial_port='/dev/ttyUSB0')
daly = Daly(db_table="Daly", serial_port='/dev/ttyUSB0')

if __name__ == '__main__':
    while True:

        ok = False
        juntek_data = juntek.read_actual_data()
        if juntek_data:
            if juntek.write2db(conn_obj=conn, data=juntek_data):
                ok = True
            juntek.mqtt_publish(ok=ok, data=juntek_data)
            print(juntek.format_report(juntek_data))

        sleep(0.5)

        ok = False
        EAsun_data = easun.read_actual_data()
        if EAsun_data:
            if easun.write2db(conn_obj=conn, data=EAsun_data):
                ok = True
            easun.mqtt_publish(ok=ok, data=EAsun_data)
            for par, val in EAsun_data.items():
                print(f"{par+':':<21} {str(val)}")

        sleep(0.5)

        ok = False
        daly_data = daly.read_actual_data()
        if daly_data:
            if daly.write2db(conn_obj=conn, data=daly_data):
                ok = True
            daly.mqtt_publish(ok=ok, data=daly_data)
            print(daly.format_report(daly_data))

        try:
            sleep(0.5)
        except KeyboardInterrupt:
            break

conn.close()
