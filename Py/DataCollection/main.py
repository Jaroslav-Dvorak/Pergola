from time import sleep
import json
import psycopg2
from Juntek import Juntek
from EAsun import EAsun


with open("../db_conf.json", "r") as f:
    raw = f.read()
    conn_params = json.loads(raw)

conn = psycopg2.connect(**conn_params)
conn.set_session(autocommit=True)

juntek = Juntek(db_table="Juntek", serial_port='/dev/ttyUSB0')
easun = EAsun(db_table="EAsun", serial_port='/dev/ttyUSB1')

if __name__ == '__main__':
    while True:

        ok = False
        if juntek.read_data():
            if juntek.write2db(conn_obj=conn):
                ok = True
        juntek.mqtt_publish(ok=ok)
        print(juntek)

        ok = False
        EAsunData = easun.read_actual_data()
        if EAsunData:
            if juntek.write2db(conn_obj=conn):
                ok = True

        for par, val in EAsunData.items():
            print(f"{par+':':<21} {str(val)}")

        try:
            sleep(1)
        except KeyboardInterrupt:
            break

conn.close()
