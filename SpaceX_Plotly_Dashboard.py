import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

spacex_df=pd.read_csv('spacex_launch_dash.csv')

max_payload=spacex_df['Payload Mass (kg)'].max()

min_payload = spacex_df['Payload Mass (kg)'].min()

spacex_pie=spacex_df[['Launch Site','class']]

sites_list=[
    {'label':sites,'value':sites}
    for sites in np.sort(spacex_df['Launch Site'].unique())
]

app=dash.Dash(__name__)

app.layout=html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign':'center','color':'503D36', 'font_size':40}),

    html.Div([
        html.Br(),
        html.Label('All Sites'),
        html.Br(),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label':'All sites','value':'All'}]+sites_list,
            value='All',
            searchable=True,
        ),
        html.Br(),
        dcc.Graph(id='success-pie-chart'),
    ]),

    html.Div([
        html.P('Payload Range (kg)'),
        dcc.RangeSlider(id='payload-slider',
                        min=min_payload,
                        max=max_payload,
                        step=500,
                        marks={0:'0',
                               2500:'2500',
                               5000:'5000',
                               7500:'7500',
                               10000:'10000'
                               },
                        value=[min_payload,max_payload]
                        ),
        html.Div(id='payload-slider-output'),
    ]),
    html.Br(),
    html.Div([
        html.P('Scatter Plot Payload Mass (kg) vs Success and Booster Version'),
        html.Br(),
        dcc.Graph(id='success-payload-scatter-chart'),
    ]),

])

@app.callback(Output('success-pie-chart','figure'),
              Input('site-dropdown','value'))

def get_pie_chart(site):
    if site == 'All':
        fig = px.pie(spacex_pie,
                     values='class',
                     names='Launch Site',
                     title='Total Success Launches by All Sites')
        return fig
    else:
        filtered_df = spacex_pie[spacex_pie['Launch Site'] == site]
        fig = px.pie(filtered_df,
                     names='class',
                     title='Total Success Launches at site ' + str(site))
        return fig

#For the bar slider selection of mass determined by the site


#scatter plot x= payload & y=launch outcome (class) "how payload may be correlated with mission outcome for selected site(s)
#color label the booster version

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])

def get_scatter_plot(site,mass):
    if site == 'All':
        df = spacex_df[(spacex_df['Payload Mass (kg)'] >= mass[0]) & (spacex_df['Payload Mass (kg)'] <= mass[-1])]
        fig = px.scatter(df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         )
        return fig
    else:
        df = spacex_df[
            (spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'] >= mass[0]) &
            (spacex_df['Payload Mass (kg)'] <= mass[-1])]

        fig = px.scatter(df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                       )
        return fig

if __name__=='__main__':
    app.run_server(debug=True)
