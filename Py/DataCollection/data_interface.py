import json
from datetime import timezone
import psycopg2

with open("../db_conf.json", "r") as f:
    raw = f.read()
    conn_params = json.loads(raw)

conn = psycopg2.connect(**conn_params)
conn.set_session(autocommit=True)


def write2db(data, db_table):
    keys = ", ".join(data.keys())
    values = [str(val) for val in data.values()]
    values = ", ".join(values)
    sqlstr = f'INSERT into public."{db_table}" ({keys}) VALUES ({values})'

    try:
        with conn.cursor() as cursor:
            cursor.execute(sqlstr)
    except Exception as e:
        print(e)
        return
    else:
        return True


def read_energy(time_from, time_to):
    time_from = time_from.astimezone(timezone.utc).isoformat()
    time_to = time_to.astimezone(timezone.utc).isoformat()
    print(time_from)
    print(time_to)
    sqlstr = f"SELECT MAX(energy)-MIN(energy) AS energy FROM \"D69\" " \
             f"WHERE time BETWEEN '{time_from}' AND '{time_to}'"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sqlstr)
            result = cursor.fetchone()
    except Exception as e:
        print(e)
        return
    else:
        return result[0]
