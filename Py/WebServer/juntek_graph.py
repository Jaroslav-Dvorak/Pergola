import json
from datetime import datetime
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine


green = "rgb(18, 94, 3)"
green_light = "rgb(52, 130, 38)"
red = 'rgba(255, 0, 0, 0.5)'
orange = 'rgb(237, 159, 43)'
blue = "rgb(4, 72, 207)"


def juntek_graph(df):

    df["voltage"] = df["voltage"]/100
    df["current"] = df["current"]/100
    df["power"] = df["voltage"]*df["current"]
    df["charged"] = df["charged"]/100
    df["charging"] = df["power"].clip(lower=0)
    df["discharging"] = df["power"].clip(upper=0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df["time"], y=df["charging"], name="charging", fill='tozeroy', fillcolor=green, line=dict(color=green)))
    fig.add_trace(go.Scatter(x=df["time"], y=df["discharging"], name="discharging", fill='tozeroy', fillcolor=red, line=dict(color=red)))
    fig.add_trace(go.Scatter(x=df["time"], y=df["charged"], name="charged", yaxis="y2", line=dict(color=orange)))
    fig.add_trace(go.Scatter(x=df["time"], y=df["voltage"], name="voltage", yaxis="y3", line=dict(color=blue)))

    fig.update_layout(xaxis=dict(domain=[0.0, 0.95], showgrid=False),
                      yaxis=dict(titlefont=dict(color=green), tickfont=dict(color=green), range=[-200, 1000], showgrid=False),
                      yaxis2=dict(titlefont=dict(color=orange), tickfont=dict(color=orange), range=[-26, 130], tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                  anchor="free", overlaying="y", side="right", position=0.97, showgrid=False),
                      yaxis3=dict(titlefont=dict(color=blue), tickfont=dict(color=blue), range=[0, 29.5], tickvals=[22, 23, 24, 25, 26, 27, 28, 29],
                                  anchor="x",  overlaying="y", side="right", showgrid=False),
                      )
    fig.update_layout(template="plotly_dark")
    fig.update_layout(title_text="", height=900)
    return fig
    
    
with open("../db_conf.json", "r") as f:
    raw = f.read()
conn_params = json.loads(raw)

db = conn_params["database"]
usr = conn_params["user"]
psw = conn_params["password"]
adr = conn_params["host"]
port = conn_params["port"]

engine = create_engine(f'postgresql://{usr}:{psw}@{adr}:{port}/{db}')


def get_data(time_start, time_end):
    time_end = datetime.fromisoformat(time_end)
    time_end = time_end.replace(hour=23, minute=59, second=59, microsecond=999999)
    query = 'SELECT * FROM public."Juntek" '
    query += f"WHERE time > '{time_start}' AND time <= '{time_end}'"
    df = pd.read_sql(con=engine, sql=query)
    return df
