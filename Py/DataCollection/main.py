from time import sleep
import json
import psycopg2
from Juntek import Juntek


with open("../db_conf.json", "r") as f:
    raw = f.read()
    conn_params = json.loads(raw)

conn = psycopg2.connect(**conn_params)
conn.set_session(autocommit=True)

juntek = Juntek()

if __name__ == '__main__':
    while True:

        ok = False
        if juntek.read_data(serial_port='/dev/ttyUSB0'):
            if juntek.write2db(conn_obj=conn, db_table="Juntek"):
                ok = True
        juntek.mqtt_publish(ok=ok)
        print(juntek)

        try:
            sleep(3)
        except KeyboardInterrupt:
            break

conn.close()
