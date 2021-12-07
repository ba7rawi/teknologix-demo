import pandas as pd 
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)


df = pd.read_csv('intro_bees.csv')
app.layout = html.Div([
    html.H1("Hello from dash", style = {'text-align':'center'}),
    dcc.Dropdown(id="slct_year", 
                options = [
                    {'label':'2015', "value":2015},
                    {'label':'2016', "value":2016},
                    {'label':'2017', "value":2017},
                    {'label':'2018', "value":2018},
                    
                ],
                value = 2015,
                style={'width': "40%"},
    ),
    html.Div(id="output_container", children = []),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure = {}, hoverData ={'v':23}),
])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]
    
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=dff['state_code'],
            z=dff["Pct of Colonies Impacted"].astype(float),
            colorscale='Reds',
        )]
    )
    
    fig.update_layout(
        title_text="Bees Affected by Mites in the USA",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)