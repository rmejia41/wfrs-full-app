# Final App
import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly

df = pd.read_csv('C:/Users/Biu9/OneDrive - CDC/WFRS/dash_apps/wfrs_app_yearly_scatter.csv')
df['year'] = df['year'].astype('int64')
df['state'] = df['state'].astype(str)

# ---------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server=app.server

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Br(),
    html.H2('WFRS Surveillance Dashboard', style={'textAlign': 'center', 'fontsize': '80px'}),
    html.H3('Division of Oral Health, Centers for Disease Control', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dpdn2', value=['Alabama', 'Arkansas'], multi=True,
                         options=[{'label': x, 'value': x} for x in
                                  df.state.unique()]),
            html.Br(),
            html.Div([
                dcc.Graph(id='pie-graph', figure={}, className='six columns'),
                dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                          config={
                              'staticPlot': False,  # True, False
                              'scrollZoom': True,  # True, False
                              'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                              'showTips': True,  # True, False
                              'displayModeBar': True,  # True, False, 'hover'
                              'watermark': True,
                              # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                          },
                          className='six columns',
                          ),
            ]),
            dbc.Tab([
                html.Ul([
                    html.Br(),
                    html.Li(
                        'The Water Fluoridation Reporting System (WFRS) is an online tool that helps states manage the quality of their water fluoridation programs. WFRS information is also the basis for national surveillance reports that describe the percentage of the U.S. population on community water systems who receive optimally fluoridated drinking water'),
                    html.Li(['Fluoridation Statistics: ',
                             html.A('https://www.cdc.gov/fluoridation/statistics/reference_stats.htm',
                                    href='https://www.cdc.gov/fluoridation/statistics/reference_stats.htm')
                             ]),
                ]),
            ]),
        ]),
    ]),
])


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(state_chosen):
    dff = df[df.state.isin(state_chosen)]
    fig = px.scatter(data_frame=dff, x='year', y='pop_cws_fl', color='state',
                     labels={
                         "pop_cws": "CWS Population",
                         "pop_fl_water": "Fluoridated Water Population",
                         "region": "Region",
                         "state": "State",
                         "pop_cws_fl": "% Population Fluoridated Water"
                     },
                     custom_data=['state', 'region'])
    fig.update_traces(mode='lines+markers')
    return fig


# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, state_chosen):
    if hov_data is None:
        dff2 = df[df.state.isin(state_chosen)]
        dff2 = dff2[dff2.year == 2000]
        print(dff2)
        fig2 = px.pie(data_frame=dff2, values='pop_cws_fl', names='state',
                      labels={  # replaces default labels by column name
                          "state": "State", "region": "Region", "pop_fl_water": "Fluoridated Water Population",
                          "pop_cws_fl": "% Population Fluoridated Water"},
                      title='% CWS Population Served with Fluoridated Water')
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.state.isin(state_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(data_frame=dff2, values='pop_fl_water', names='state',
                      labels={  # replaces default labels by column name
                          "state": "State", "region": "Region", "pop_fl_water": "Fluoridated Water Population",
                          "pop_cws_fl": "% Population Fluoridated Water"
                      })
        return fig2


if __name__ == '__main__':
    app.run_server(debug=False, port=8060)