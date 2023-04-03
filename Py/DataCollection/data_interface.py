import json
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
