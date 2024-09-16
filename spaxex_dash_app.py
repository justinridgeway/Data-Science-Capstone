# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'VAFB SLC-4E','value':'VAFB SLC-4E' }, {'label': 'KSC LC-39A', 'value':'KSC LC-39A'}, {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}],value="ALL", placeholder ="Select a Launch Site Here", searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success_pie_chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"), 
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider', min=0, max=10000, step=1000, marks={0: '0',100: '100'},value=[0, 1000]),                 
                                               
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success_pie_chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    data = spacex_df
    if site_dropdown == 'ALL':        
        title='Results from all sites'       
    else:
        data = data[data['Launch Site']== site_dropdown]
        title = "Results from " + site_dropdown
    labels = ['Success', 'Failure']
    succ_fail = [0,0]
    for index, rows in data.iterrows():
        if rows['class'] == True:
            succ_fail[0]+=1
        else:
            succ_fail[1]+=1    
    fig = px.pie(succ_fail, values=succ_fail,
    names =labels,
    title=title)
    return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),Input(component_id='site_dropdown', component_property='value'), Input(component_id="payload_slider", component_property="value"))

def get_scatter_graph(site_dropdown, payload_slider):    
    data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0])  & (spacex_df['Payload Mass (kg)']<= payload_slider[1])]
    if site_dropdown != 'ALL':       
        data =data[data['Launch Site']== site_dropdown]          
    succ_fail = []
    for index, rows in data.iterrows():
        if rows['class'] == True:
            succ_fail.append(1)
        else:
            succ_fail.append(0)
    data.loc[:,'succ_fail'] = succ_fail
    title = "Fail/Success vs Payload Mass"
    fig = px.scatter(data, x='Payload Mass (kg)', y= 'succ_fail',
    color = 'Booster Version Category',title = title)    
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()


