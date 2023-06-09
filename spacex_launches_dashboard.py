import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

# Create a dash application
app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app.layout = html.Div(children=[ html.H1('Success Launches of SpaceX', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
                                html.Div([
                                # Segment 1
                                    # Add an division
                                    html.Div([
                                        # Create an division for adding dropdown helper text for launch sites
                                        html.Div(
                                            [
                                            html.H2('Launch Site:', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                        # Enter your code below. Make sure you have correct formatting.
                                        dcc.Dropdown(id='input-type', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[
                                                            {'label': 'All Sites', 'value': 'ALL'},
                                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
                                                            ],
                                                     placeholder="place holder here",
                                                     searchable=True,
                                                     style={'width':'80%', 'padding':'3px', 'font-size':'20px', 'text-align-last':'center'}),
                                            # Place them next to each other using the division style
                                            ], style={'display': 'flex'}),
                                    # Add next division 
                                    html.Div([
                                        #Adding range slider title
                                        html.Div(
                                            [
                                            html.H2('Payload Mass (Kg)', style={'margin-right': '2em'})
                                            ]
                                        ),
                                        #Adding range slider
                                        dcc.RangeSlider(id='input-slider', 
                                                     min=0,
                                                     max=10000,
                                                     step=1000,
                                                     marks={0:'0', 100:'100'},
                                                     value=[min, max])
                                            ]),  
                                          ]),
                                #Showing the pie chart, range slider and scatterplot
                                html.Div([ ], id='success-pie-chart'),
                                html.Div(id='my-range-slider', style={'margin-top': 20}),
                                html.Div([ ], id='scatter')
                                

                                ])

# Function decorator to specify function input and output
@app.callback([Output(component_id='success-pie-chart', component_property='children'),
               Output(component_id='my-range-slider', component_property='children'),
               Output(component_id='scatter', component_property='children')],
              [Input(component_id='input-type', component_property='value'),
               Input(component_id='input-slider', component_property='value'),
               Input(component_id='input-type', component_property='value'),
               Input(component_id='input-slider', component_property='value')],
              [State('success-pie-chart', 'children'),
               State('my-range-slider', 'children'),
               State('scatter', 'children')])

def get_pie_chart(entered_site, children):
    #filtered_df = spacex_df
    a=spacex_df.groupby(['Launch Site'])['class'].size()
    if entered_site == 'ALL':
        fig = px.pie(a, values='class',
        names=['CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E', 'CCAFS LC-40'], 
        title='Total Success Launches by Site')
        fig_s=px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return [dcc.Graph(figure=fig),
                dcc.Graph(figure=fig_s)]
    else:
        b = spacex_df.groupby('Launch Site').filter(lambda x : pd.Series([entered_site]).isin(x['Launch Site']).all())
        c = b.groupby(['Launch Site', 'class'])['class'].size()
        fig2=px.pie(c,
        values='class',
        names= ['0', '1'],
        title='Total Success Launches for'+entered_site)
        d = b.groupby(['Launch Site', 'Payload Mass (kg)', 'Booster Version Category', 'class']).size()
        fig_s2=px.scatter(d, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return [dcc.Graph(figure=fig2),
                dcc.Graph(figure=fig_s2)]

if __name__ == '__main__':
    app.run_server()

