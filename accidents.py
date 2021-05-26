import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv('Accidents Germany cleaned data_new.csv', sep=';')
df = df.set_index(['Time'])
#print(df)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1("Germany traffic accidents 2010 - 2019", style={'textAlign': 'center'}), width=12)
    ]),
    dbc.Row([
                dbc.Col(dcc.Dropdown(id='value_dropdown', placeholder='Enter accident injury type...',
                                     options=[{'label': 'Accidents with personal injury', 'value': 'Accidents_with_personal_injury'},
                                              {'label': 'Fatal traffic accidents', 'value': 'Fatal_traffic_accidents'},
                                              {'label': 'Seriously injured', 'value': 'Seriously_injured'},
                                              {'label': 'Slightly injured', 'value': 'Slightly_injured'}],
                                     multi=True,
                                     value=['Accidents_with_personal_injury', 'Slightly_injured']
                                     ),
                        width={'size': 8, "offset": 2, 'order': 1}
                        )
        ]),
    dbc.Row([

            dbc.Col(dcc.Graph(id='line_chart', figure={},
                              config={'displayModeBar': True}), xs=8, sm=8, md=8, lg=12, xl=12)

        ]),
    dbc.Row([

                dbc.Col(dcc.Graph(id='violin_chart', figure={},
                                  config={'displayModeBar': True}), xs=8, sm=8, md=8, lg=12, xl=12)

            ])
])


# must have Dash version 1.16.0 or higher
@app.callback(
    [Output('line_chart', 'figure'),
     Output('violin_chart', 'figure')],
    Input('value_dropdown', 'value')
)
def update_graph(value_dropdown):
    dff = df
    if not value_dropdown:
        line_chart = px.line(x=[0], y=[0], title='Number of Accidents in Germany:',
                             labels={'x': 'Year', 'y': 'Number of People'}).update_layout(showlegend=True)
        violin_chart = px.violin(x=[0], y=[0], title='Statistics of Accidents in Germany:')
        return line_chart, violin_chart
    else:
        dff = df[value_dropdown]
        line_chart = px.bar(dff, title='Number of Accidents in Germany:', log_y=True,
                            labels={'Time': 'Year', 'value': 'Number of People'})
        line_chart.update_layout(legend=dict(orientation="h", title="Legend:"))
        violin_chart = px.violin(dff, title='Statistics of Accidents in Germany:', labels={'variable': 'Type of Injury', 'value': 'Number of People'}, log_y=True).update_layout(showlegend=True)
        return line_chart, violin_chart


if __name__ == '__main__':
    app.run_server(debug=False)

