# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
df = pd.read_csv("spacex_launch_dash.csv")
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',options=[
                                {'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True,
                                ), 
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success_pie_chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0,10001,1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success_payload_scatter')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success_pie_chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_chart(sitename):
    df0 = df[['Launch Site','class']]
    if sitename == 'ALL':
        df0 = df0.groupby(['Launch Site']).sum().reset_index()
        fig = px.pie(df0, names='Launch Site', values='class',
                title='Total success launches by sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        df0=df0[df0['Launch Site']==sitename]
        df0 = df0.groupby(['class']).count().reset_index()
        fig = px.pie(df0, names='class', values='Launch Site', 
                title='Total success launches for site {}'.format(sitename)
                )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success_payload_scatter', component_property='figure'),
              [Input(component_id='site_dropdown', component_property='value'),
              Input(component_id='payload_slider', component_property='value')]
              )
def getchart(sitename,payslider):
    df0 = df[['Launch Site','Payload Mass (kg)','class','Booster Version Category']]
    df0 = df0[df0['Payload Mass (kg)']>=payslider[0]]
    df0 = df0[df0['Payload Mass (kg)']<=payslider[1]]
    if sitename == 'ALL':
        df0 = df0[['Payload Mass (kg)','class','Booster Version Category']].reset_index()
        fig = px.scatter(df0, y='class', x='Payload Mass (kg)', color='Booster Version Category', symbol='Booster Version Category',
               title='Correlation between Payload and Success for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        df0=df0[df0['Launch Site']==sitename]
        df0 = df0[['Payload Mass (kg)','class','Booster Version Category']].reset_index()
        fig = px.scatter(df0, y='class', x='Payload Mass (kg)', color='Booster Version Category', symbol='Booster Version Category',
                     title='Correlation between Payload and Success for site {}'.format(sitename)
                 )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
