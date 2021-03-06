import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

bs = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=bs)
server = app.server

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5('Thermal diffusivity(m^2/s), α'),
            dcc.Input(id='thermaldiffusivity', type='number', value=0.0000002)
        ], width={'size':4}),
        dbc.Col([
            html.H5('Time(s), t'),
            dcc.Input(id='time', type='number', value=300)
        ], width={'size':4}),
        dbc.Col([
            html.H5('Distance(m), x'),
            dcc.Input(id='distance', type='number', value=0.05)
        ], width={'size':4})
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Steps of time, nt'),
            dcc.Input(id='stepst', type='number', value=8)
        ], width={'size':4}),
        dbc.Col([
            html.H5('Steps of distance, nx'),
            dcc.Input(id='stepsx', type='number', value=10)
        ], width={'size':4}),
        dbc.Col([
            html.H5('Initial temperature of slab(K)'),
            dcc.Input(id='T0', type='number', value=273)
        ], width={'size':4})
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Temperature at the left(K)'),
            dcc.Input(id='Tl', type='number', value=373)
        ], width={'size':4}),
        dbc.Col([
            html.H5('Temperture at the right(K)'),
            dcc.Input(id='Tr', type='number', value=373)
        ], width={'size':4}),
        dbc.Col([
            html.Button('Enter', id='submit-val', n_clicks=0)
        ], width={'size':2}),
        dbc.Col(id='container-button-basic', children='', width={'size':2})
    ]),
    dbc.Row([
        dbc.Col(id='heatmap', children='', width={'size':6}),
        dbc.Col(id='dataf',children='', width={'size':6})
    ]),
    dbc.Row([
        dbc.Col(id='slidert',children='', width={'size':6}),
        dbc.Col(id='sliderx',children='', width={'size':6})
    ])
])

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('thermaldiffusivity', 'value')],
    [dash.dependencies.State('time', 'value')],
    [dash.dependencies.State('distance','value')],
    [dash.dependencies.State('stepst', 'value')],
    [dash.dependencies.State('stepsx', 'value')])
def update_output(n_clicks,v1,v2,v3,v4,v5):
    v = str((v1*v2*(v5**2))/(v4*(v3**2)))
    return html.Div([html.P("Make sure β below is less than or equal to 0.5"), html.P("β = α(t/nt)/(x/nx)^2"),html.P("β="+ v)])
@app.callback(
    dash.dependencies.Output('heatmap', 'children'),
    dash.dependencies.Output('dataf', 'children'),
    dash.dependencies.Output('slidert', 'children'),
    dash.dependencies.Output('sliderx', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('thermaldiffusivity', 'value')],
    [dash.dependencies.State('time', 'value')],
    [dash.dependencies.State('distance','value')],
    [dash.dependencies.State('stepst', 'value')],
    [dash.dependencies.State('stepsx', 'value')],
    [dash.dependencies.State('T0', 'value')],
    [dash.dependencies.State('Tl', 'value')],
    [dash.dependencies.State('Tr', 'value')])
def update_graphT(n_clicks,v1,v2,v3,v4,v5,v6,v7,v8):

    nt = v4 + 1
    nx = v5 + 1

    deltat = v2/v4
    deltax = (v3/v5)**2
    L = v1*deltat/deltax

    Tt=np.random.rand(nt,nx)

    for i in range(nt):
        Tt[i][1:nx-1]= v6
        Tt[i][0] = v7
        Tt[i][nx-1] = v8

    for j in range(nt-1):
        for i in range(nx-2):
            Tt[j+1][i+1] = Tt[j][i+1] + L*(Tt[j][i+2]-2*Tt[j][i+1]+Tt[j][i])
    df = pd.DataFrame(Tt)
    df.shape[0]
    df.shape[1]
    x1 = list(range(0,df.shape[0]))*df.shape[1]
    y1 = []
    z1 = []
    for i in range(df.shape[1]):
        y1 = y1 + [i]*(df.shape[0])

    for i in range(df.shape[1]):
        z1 = z1 + df[i].values.tolist()

    df1 = pd.DataFrame([x1,y1,z1]).T
    df1.columns = ['Δt','Δx','Temperature(K)']
    fig = px.scatter_3d(df1,x='Δx', y='Δt',z='Temperature(K)', title="1d Heat Equation")
    figt = px.scatter(df1, x='Δx', y='Temperature(K)', animation_frame='Δt', range_y=[min(v6,v7,v8)-10, max(v6,v7,v8)+10],title="Distance Graph With Time Slider")
    figx = px.scatter(df1, x='Δt', y='Temperature(K)', animation_frame='Δx', range_y=[min(v6,v7,v8)-10, max(v6,v7,v8)+10],title="Time Graph With Distance Slider")
    figh = px.imshow(df, labels=dict(x='Δx', y='Δt', color='Temperature(K)'),title="1d Heat Map")

    return dcc.Graph(figure=figh), dcc.Graph(figure=fig), dcc.Graph(figure=figt), dcc.Graph(figure=figx)

if __name__ == '__main__':
    app.run_server()
