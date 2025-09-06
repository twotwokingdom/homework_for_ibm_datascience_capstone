import pandas as pd
import dash
from dash import html
from dash import dcc
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
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),

# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)

                    html.Br(),

                    dcc.Dropdown(id='site-dropdown',
                    options=[{'label':'All Sites', 'value':'ALL'}] + \
                    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                    value='ALL',
                    placeholder="place holder here",
                    searchable=True
                    ),

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
                    html.Div(dcc.Graph(id='success-pie-chart')),
                    html.Br(),
# Function decorator to specify function input and output
  
                    html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)
                    dcc.RangeSlider(
                    id='payload-slider',
                    min=0, max=max_payload, step=1000,
                    marks={int(i):str(int(i)) for i in
                    range(0, int(max_payload)+1, int(max_payload/5))},
                    value=[min_payload, max_payload]
),
 # TASK 4: 添加散点图显示有效载荷与发射成功的关系
                    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

  

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# TASK 2: 饼图回调函数
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df = spacex_df[spacex_df['class']==1]
        fig = px.pie(df, names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        df = spacex_df[spacex_df['Launch Site']==entered_site]
        counts = df['class'].value_counts().reset_index()
        counts.columns=['class','count']
        counts['class']=counts['class'].map({1:'Success',0:'Failure'})
        fig = px.pie(counts, names='class', values='count',
                     title=f'Success vs Failure at {entered_site}')
    return fig

# 散点图回调
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    dff = spacex_df[(spacex_df['Payload Mass (kg)']>=low)&
                    (spacex_df['Payload Mass (kg)']<=high)]
    if selected_site!='ALL':
        dff = dff[dff['Launch Site']==selected_site]
    if dff.empty:
        return px.scatter(title='No data for selection')
    fig = px.scatter(dff, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload vs Launch Success',
                     labels={'class':'Launch Success',
                             'Payload Mass (kg)':'Payload Mass (kg)'})
    return fig 
  

# Run the app
if __name__ == '__main__':
    app.run()