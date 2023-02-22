from datetime import date, timedelta
import locale
import platform
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from juntek_graph import juntek_graph, get_data

if platform.system() == 'Windows':
    LOCALE = 'cs'
else:
    LOCALE = ('cs_CZ', 'UTF-8')

locale.setlocale(category=locale.LC_ALL, locale=LOCALE)
external_scripts = ["assets/plotly-locale-cs--latest.js"]

app = Dash(__name__,
           external_scripts=external_scripts,
           title='Pergola',
           update_title=None,
           suppress_callback_exceptions=True,)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    output=Output("page-content", "children"),
    inputs=Input("url", "pathname"),
)
def display_page(pathname):
    datepicker = dcc.DatePickerRange(id='rangepicker',
                                     start_date=date.today()-timedelta(days=1),
                                     end_date=date.today(),
                                     display_format='D.M.YY',
                                     start_date_placeholder_text='M-D-Y-Q',
                                     )
    ok_button = html.Button("-->OK<--", id="ok")

    layout = html.Div(children=[
        dcc.Graph(id='juntek_graph', config={"locale": "cs"}),
        html.Div(children=[datepicker, ok_button]),

    ])
    return layout


@app.callback(
    output=Output(component_id='juntek_graph', component_property='figure'),
    inputs=Input(component_id="ok", component_property="n_clicks"),
    state=[State(component_id="rangepicker", component_property="start_date"),
           State(component_id="rangepicker", component_property="end_date")]
)
def render_graph(ok_buton, start_date, end_date):
    df = get_data(start_date, end_date)
    fig = juntek_graph(df=df)
    return fig


if __name__ == '__main__':
    app.run_server("0.0.0.0", debug=True, )
