import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = 0

with open("data_logs.csv", "r") as f:
    df = pd.read_csv(f, 
                    header=None, 
                    names=['timestamp', 'temp', 'humi'],
                    index_col=False,
                    )
    df['timestamp'] =  pd.to_datetime(df['timestamp'], format="%d-%m-%Y %H:%M")
    df['year'] = pd.DatetimeIndex(df['timestamp']).year
    df['month'] = pd.DatetimeIndex(df['timestamp']).month
    df['day'] = pd.DatetimeIndex(df['timestamp']).day
    df['date'] =  df['timestamp'].dt.date
    df['time'] =  df['timestamp'].dt.time
    df = df[::-1]
    df = df.reset_index(drop=True)
    f.close()


def update_df():
    with open("data_logs.csv", "r") as f:
        df = pd.read_csv(f,
                        header=None, 
                        names=['timestamp', 'temp', 'humi'],
                        index_col=False,
                        )
        df['timestamp'] =  pd.to_datetime(df['timestamp'], format="%d-%m-%Y %H:%M")
        df['year'] = pd.DatetimeIndex(df['timestamp']).year
        df['month'] = pd.DatetimeIndex(df['timestamp']).month
        df['day'] = pd.DatetimeIndex(df['timestamp']).day
        df['date'] =  df['timestamp'].dt.date
        df['time'] =  df['timestamp'].dt.time
        df=df[::-1]
        df = df.reset_index(drop=True)
        f.close()
    return df





app.layout = html.Div(children=[
    html.Label('Range'),
    dcc.Dropdown(
        id='range-drop',
        options=[{'label': str(k), 'value': str(k)} for k in ['All', *df['date'].drop_duplicates()]],
        value='All'
    ),

    html.Div(id='range-drop-number'),
    

    html.H3(children='Home Temprature',
        style={
            'textAlign': 'center',
            }
        ),


    dcc.Graph(
        id='temp-graph',
        figure={
            'data': [
                go.Scatter(
                y = df['temp'], 
                x = df['timestamp'],
                mode='markers+lines',
                marker={
                        'line': {'width': 1.0, 'color': 'red'},
                        'symbol': 'diamond',
                        'size' : 3,
                       },
                line={
                        'width': 1.0, 'color': 'red'
                    },
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Temperature C'},
            )
        }
    ),

    html.H3(children='Home Humidity',
        style={
            'textAlign': 'center',
            }
        ),

    dcc.Graph(
        id='humi-graph',
        figure={
            'data': [
                go.Scatter(
                y = df['humi'], 
                x = df['timestamp'],
                mode='markers+lines',
                marker={
                        'line': {'width': 1.0, 'color': 'blue'},
                        'symbol': 'diamond',
                        'size' : 3,
                       },
                line={
                        'width': 1.0, 'color': 'blue'
                    },
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Humidity %'},
                )
        }
    )
])

@app.callback(
    [Output('range-drop-number', 'children'),
     Output('temp-graph', 'figure'),
     Output('humi-graph', 'figure'),
     Output('range-drop', 'options')],
    [Input('range-drop', 'value')])
def update_range(value):
    df = update_df()
    if value=='All':
        return  'Current Range is "{}"'.format(str(value)), { ###
                'data': [
                    go.Scatter(
                    y = df['temp'],
                    x = df['timestamp'],
                    mode='markers+lines',
                    marker={
                            'line': {'width': 1.0, 'color': 'red'},
                            'symbol': 'diamond',
                            'size' : 3,
                        },
                    line={
                            'width': 1.0, 'color': 'red'
                        },
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Temperature C'},
                )
                }, { ###
                'data': [
                    go.Scatter(
                    y = df['humi'],
                    x = df['timestamp'],
                    mode='markers+lines',
                    marker={
                            'line': {'width': 1.0, 'color': 'blue'},
                            'symbol': 'diamond',
                            'size' : 3,
                        },
                    line={
                            'width': 1.0, 'color': 'blue'
                        },
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Humidity %'},
                    )
                },[ ###
                        {'label': str(k), 'value': str(k)} for k in ['All', *df['date'].drop_duplicates()]]
    else:
        date = pd.to_datetime(value, format="%Y-%m-%d").date()
        this_df=df.loc[df['date']==date]
        return  'Current Range is "{}"'.format(str(value)), { ###
                'data': [
                    go.Scatter(
                    y = this_df['temp'],
                    x = this_df['timestamp'],
                    mode='markers+lines',
                    marker={
                            'line': {'width': 1.0, 'color': 'red'},
                            'symbol': 'diamond',
                            'size' : 3,
                        },
                    line={
                            'width': 1.0, 'color': 'red'
                        },
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Temperature C'},
                )
                }, { ###
                'data': [
                    go.Scatter(
                    y = this_df['humi'],
                    x = this_df['timestamp'],
                    mode='markers+lines',
                    marker={
                            'line': {'width': 1.0, 'color': 'blue'},
                            'symbol': 'diamond',
                            'size' : 3,
                        },
                    line={
                            'width': 1.0, 'color': 'blue'
                        },
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Humidity %'},
                    )
                },[ ###
                        {'label': str(k), 'value': str(k)} for k in ['All', *df['date'].drop_duplicates()]]


if __name__ == '__main__':
    update_df()
    #app.run_server(host='0.0.0.0', debug=True)
    app.run_server(host='0.0.0.0')

