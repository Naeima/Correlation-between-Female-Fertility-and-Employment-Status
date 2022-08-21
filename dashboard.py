

'''This code creates an interactive dashboard to visualise a study about the relationship between the female fertility and her employment status.
multiple datasets were selected and analyised, key findings were communicated.

The visualisations types and dashboard ideas were adapted from this coursework's module(CM212). '''
'''This code was adapted from:Udemy. 2019. Online Courses - Anytime, Anywhere | Udemy.[online] Available at
https://www.udemy.com/interactive-python-dashboards-with-plotly-and-dash/learn/lecture/9527932#questions/6871174 [Accessed 20 Apr. 2019]'''

'''To run:
........... python dashboad.py'''

# Importing required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
from scipy import stats
import plotly.figure_factory as ff
import chart_studio.plotly as py
import numpy as np
from numpy import random
import plotly

# Open and read the dataset using pandas.
URL = 'https://raw.githubusercontent.com/Naeima/Datasets/master/master.csv' 
df = pd.read_csv(URL,sep=',',error_bad_lines=False)

# Intialize the dashboard
app = dash.Dash()
server = app.server


# Data for selected region from the dropdown
region_options=[]
for region in df['Region'].unique():
    region_options.append({'label': str(region),'value': region})
# Data for seleted year from the silder
year_options=[]
for year in df['Year'].unique():
    year_options.append({'label': year,'value': year})

# Dashboard layout
''' Image was taken from:[16] resarchgate.net. 2019. Map of Nuts 1. [online] Available at: 
                https://www.researchgate.net/figure/Map-of-NUTS-1-regions-in-the-UK-3_fig1_328861101. [Accessed 22 April 2019].'''
app.layout=html.Div([ html.A([
                html.Img(# inserting UK map image by region
                src='https://www.researchgate.net/profile/Bethany_Toma2/publication/328861101/figure/download/fig1/AS:691532764045312@1541885667268/Map-of-NUTS-1-regions-in-the-UK-3.ppm',
      
                style={
                    'height' : '50%',
                    'width' : '35%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding': '0px 20px 20px 20px','display': 'inline-block', 'vertical-align': 'middle'}),
               
                # Inserting the title  and introduction
                html.Div([html.Div('Female Fertility and Employment Status in the UK',
                style={'color':'black','margin':50, 'width':'70%', 'font-size':38}),

                html.Div(''' According to a study publised by the Institute for Fiscal Studies in [1] stated that
                   "Over the past 40 years, the UK has seen an almost continual 
                    rise in the proportion of women in employment. The Employment Rate among
                    women of ‘prime working age’ (aged 25-54) is up from 57% in 1975 to a record 
                    high of 78% in 2017."''',
                    style={'color':'black','margin':50, 'width':'70%','font-size':24}),
                
                html.Div('''On the other hand, The Office for National Statistics [2] said that
                    "The Total Fertility Rate (TFR³) for England and Wales
                    decreased in 2017 to an average of 1.76 children per woman from 1.81 in 2016, declining 
                    for the fifth consecutive year, from 1.94 in 2012."''',
                    style={'color':'black','margin':50, 'width':'70%', 'font-size':24}),
                
                html.Div('''This study aims to statistically explore possible relationships between female fertility and employment status in the regions
                    of the United Kingdoms. In other words, we propose to observe correlations between the rate of female fertility and employment for each region each year, starting from 2008 up to 2016.
                    We extracted the female fertility rates and female employment status rates' datasets by regions for each year for the specified period
                    from various governmental institutions websites in [4],[5],[6] and [7].''',
                    style={'color':'black','margin':50, 'width':'70%', 'font-size':24}),

                html.Div('''UK map displayed to the left shows each region location, this image was sourced from [3]''',
                    style={'color':'black','margin':50, 'width':'90%','font-size':24})],      
                    
                    # this styles the outermost Div:
                    style={'width': '70%', 'display': 'left', 'height':600, 'vertical-align': 'right', 'color':'Black'}), html.Hr(), html.Hr(),html.Hr(),
                  
                # Defining the first two graphs function.        
                html.Div('''The interactive stacked graphs below are displaying the Female Employment, Fertility and Unemployment Rates for each region,
                    the year slider below it, allows the user to select the year of interest and display these region's data for the selected year.
                    Extreme values observerd for all regions from analysis are as follows: Fertility Rate: highest is West Midlands and lowest is Scotland.
                    Employment Rate: highest is South West and lowest is London. Unemployment Rate: highest is London and lowest is East. ''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':24}),

                # Adding the year slider to the two main stacked bar graph.
                html.Div([dcc.Graph(id='Main')],style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'}),html.Div([dcc.Graph(id='Main2')],
                style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'}),html.Div(
                dcc.Slider(id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()}))],
                style={'width': '50%', 'margin': 100, 'padding': '0 20'}),html.Hr(),
                # Defining the correlations graphs.
                html.Div('''The first three scatter graphs below show the trends over years for the Employment, Fertility and Unemployment Rate,
                the rest two graphs after them are displaying the relationship between Fertility and Employment Rate, Fertility and 
                Unemployment Rate respectively, when a region is selected from the drop-down region-picker, all graphs interact together
                and display the corresponding information of the selected region.''',
                style={'color':'black','margin':50, 'width':'90%', 'font-size':24}),
                #adding the region picker to the correlatins graphs.
                html.Div([dcc.Dropdown(id='region-picker', options=region_options, value=df['Region'].min())]), html.Div([dcc.Graph(id='graph3')], 
                style={'width': '32%', 'display': 'inline-block', 'padding': '0 20'}),html.Div([dcc.Graph(id='graph1')],
                style={'width': '32%', 'display': 'inline-block', 'padding': '0 20'}),html.Div([dcc.Graph(id='graph2')],
                style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'right','padding': '0 20'}),html.Div([dcc.Graph(id='graph4')],
                style={'width': '49%','display': 'inline-block', 'padding': '0 20'}), html.Div([dcc.Graph(id='graph5')],
                style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'right', 'padding': '0 20'}),
                
                
                # Adding conclusion
                html.Div('''Key findings: The non-parametric statistical test, Spearman's Rank Correlation Coefficient (Rs) was applied on the combined datasets,
                it is a technique which can be used to summarise the strength and direction (negative or positive) of a relationship between two variables. 
                The result will always be between 1 and minus 1, The closer (Rs) is to +1 or -1, the stronger the likely correlation.
                The test results suggested that between years 2008 to 2016, there was a strong positive correlation of (Rs=0.86) between Female Fertility and Unemployment Rate 
                in the United Kingdom. In contrast, a relatively weak negative correlation of (Rs=-0.3) was observed between her Fertility and Employment Rate''',
                style={'color':'black','margin':50, 'width':'90%', 'font-size':24}),
                
                html.Div('''In the nutshell, the test results performed and the scatter plots visualised suggested that for the period between 2008 to 2016, there was
                continual rise in the proportion of women in employment and a strong drop in both fertility and unemployment.
                The findings may indicate that female unemployment tends to increase fertility, however, in statistics, it's a logical fallacy to 
                assume that female unemployment causes the increase in fertility because correlation does not imply causation.''',
                style={'color':'black','margin':50, 'width':'90%', 'font-size':24}),html.Hr(),
                
                # Adding references list.
                html.Div('''[1]	Roantree, B and Vira, K. 2018. Institute for Fiscal Studies. 2018.
                    The rise of rise of women's employment in the UK. [Online] Available at: 
                    https://www.ifs.org.uk/publications/12951. [Accessed 30 April 2019].''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[2] Haines, N., 2018. Births in England and Wales: 2016. Births in England and Wales: 2017 Live births,
                    stillbirths and the intensity of childbearing, measured by the Total Fertility Rate., [Online]. statistical 
                    bulletin, 3 0f 10.[Accessed 22 April 2019].''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[3] resarchgate.net. 2019. Map of Nuts 1.[ONLINE] 
                    Available at: https://www.researchgate.net/figure/Map-of-NUTS-1-regions-in-the-UK-3_fig1_328861101. [Accessed 22 April 2019]''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[4] Ons.gov.uk. 2019 Births by mothers’ usual area of residence in the UK - Office for
                    National Statistics.. [online] Available at: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriag
                    es/livebirths/datasets/birthsbyareaofusualresidenceofmotheruk [Accessed 20 Apr.2019].''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[5] Powell, A. 2019. Labour market statistics: UK regions and countries. [Online] Researchbriefings.parliament.uk. Available at:
                    https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7950#fullreport [Accessed 20 Apr. 2019]''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[6] Statista. 2019. Total Fertility Rate Scotland 2017 | Statistic. [Online] Available at: 
                    https://www.statista.com/statistics/367781/total-fertility-rate-in-scotland/[Accessed 20 Apr. 2019]''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                html.Div('''[7] Statista. 2019. Northern Ireland: Fertility Rate 2003-2017 | Statistic. [Online] Available at: https://www.statista.com/statistics/383835/northern-ireland-fertilityrate-timeline/ [Accessed 20 Apr. 2019]''',
                    style={'color':'black','margin':50, 'width':'90%', 'font-size':12}),
                ])
                

# Dashboard calling the first stacked bar graph. 
@app.callback(Output('Main','figure'),[Input('year-slider','value')])
#This code plots takes in the data for fertility and employment and output them on stached bar graph by region, the year slider allows year change.
def main_graph(selected_year):
    sorted_df= df[df['Year']==selected_year]
    data=[]
    for region in sorted_df['Region'].unique():
        df_by_region = sorted_df[sorted_df['Region']==region]
        data.append(go.Bar(x=df_by_region['Region'], y= df_by_region['Employment Rate'],name=region+' '+'Employment Rate',
        marker=dict(color='rgb(70,130,180)'),width=0.9, opacity=0.3, text= df_by_region['Employment Rate'],textposition = 'auto'))      
        data.append(go.Bar(x=df_by_region['Region'], y= df_by_region['Fertility Rate'],name= region+' '+'Fertility Rate',
        marker=dict(color='rgb(218, 112, 214)'),width=0.9,text= df_by_region['Fertility Rate'],textposition = 'auto'))
    return {'data':data,'layout':go.Layout(barmode='group', bargap=0.15, bargroupgap=0.1,showlegend=False,
        title= 'Employment and Fertility Rate by Region'+' '+ str(selected_year),
        yaxis={'title': 'Fertility & Employment : '+' '+ str(selected_year),'type':'linear'})}

# Dashboard calling the second stacked bar graph. 
@app.callback(Output('Main2','figure'),[Input('year-slider','value')])
#This code plots takes in  the data for fertility and unemployment and output them on stached bar graph by region, the year slider allows year changing.
def main_graph(selected_year):
    sorted_df= df[df['Year']==selected_year]
    data=[]
    for region in sorted_df['Region'].unique():
        df_by_region = sorted_df[sorted_df['Region']==region] 
        data.append(go.Bar(x=df_by_region['Region'], y= df_by_region['Unemployment Rate'], name=region+' '+'Unemployment Rate',
        marker=dict(color='rgb(112, 128, 144)'), width=0.9,opacity=0.3, text= df_by_region['Unemployment Rate'],textposition = 'auto'))
        data.append(go.Bar(x=df_by_region['Region'], y= df_by_region['Fertility Rate'],name= region+' '+'Fertility Rate',
        marker=dict(color='rgb(218, 112, 214)'),width=0.9,text= df_by_region['Fertility Rate'],textposition = 'auto'))
    return {'data':data,'layout':go.Layout(barmode='group', bargap=0.15, bargroupgap=0.1,showlegend=False,
        title= 'Fertility and Unemployment Rate by Region'+' '+ str(selected_year),
        yaxis={'title': 'Fertility & Unemployment : '+' '+ str(selected_year),'type':'linear'})}

                            
# Dashboard calling the  Female Employment Rate times series
@app.callback(Output('graph3','figure'),[Input('region-picker','value')])
#This code takes in the employment data and plot its trend over the year range, the dropdown allows region changing.
def update_figure(picked_region):
    sorted_df= df[df['Region']==picked_region]
    data=[]
    for year in sorted_df['Year'].unique():
        df_by_year = sorted_df[sorted_df['Year']==year]
        data.append(go.Scatter(x=df_by_year['Year'], y= df_by_year['Employment Rate'], mode = 'markers+lines',
        opacity = 0.7,  marker = {'size': 15,'color': 'rgb(135, 206, 235)','symbol': 'pentagon','line': {'width': 2}},name= picked_region))
    return {'data':data,'layout':go.Layout(title= 'Female Fertility Rate ' +' '+ picked_region, plot_bgcolor= 'rgb(245,245,245)', showlegend= False,
            yaxis={'title': 'Employment Rate'+' '+ picked_region,'type':'linear'},
            margin={'l': 50, 'b': 20, 't': 170, 'r': 5}, height=500, hovermode='closest')}
    

# Dashboard calling the Female  Fertility Rate time series 
@app.callback(Output('graph1','figure'),[Input('region-picker', 'value')])
#This code takes in the fertility data and plot its trend over the year range, the dropdown allows region changing.
def update_figure2(picked_region):
    sorted_df= df[df['Region']==picked_region]
    data=[]
    for year in sorted_df['Year'].unique():
        df_by_year = sorted_df[sorted_df['Year']==year]
        data.append(go.Scatter(x=df_by_year['Year'], y= df_by_year['Fertility Rate'], mode ='markers+lines',connectgaps=True,
        opacity = 0.7,marker = {
                        'size': 15,
                        'color': 'rgb(218, 112, 214)',
                        'symbol': 'pentagon',
                        'line': {'width': 2}
                        }, name= picked_region))

    return {'data':data,'layout':go.Layout(title= 'Female Fertility Rate ' +' '+ picked_region, plot_bgcolor= 'rgb(245,245,245)', showlegend= False,
            yaxis={'title': 'Fertility Rate'+' '+ picked_region,'type':'linear'},
            margin={'l': 50, 'b': 20, 't': 170, 'r': 5}, height=500, hovermode='closest')}


# Dashboard calling the Female Unempployment Rate 
@app.callback(Output('graph2','figure'),[Input('region-picker', 'value')])
#This code takes in the unemployment data and plot its trend over the year range, the dropdown allows region changing.
def update_figure3(picked_region):
    sorted_df= df[df['Region']==picked_region]  
    data=[]
    for year in sorted_df['Year'].unique():
        df_by_year = sorted_df[sorted_df['Year']==year]
        data.append(go.Scatter(x=df_by_year['Year'], y= df_by_year['Unemployment Rate'], mode = 'markers+lines',connectgaps=True,
        opacity = 0.7, marker = {
                        'size': 15,
                        'color': 'rgb(112, 128, 144)',
                        'symbol': 'pentagon',
                        'line': {'width': 3},
                        }, name= picked_region))
        
    return {'data':data,'layout':go.Layout(title= 'Female Uemployment Rate '+''+ picked_region, plot_bgcolor= 'rgb(245,245,245)', showlegend= False,
            yaxis={'title': 'Unemployment Rate '+''+ picked_region, 'type':'linear' },
            margin={'l': 50, 'b': 20, 't': 170, 'r': 5},
            height=500,
            hovermode='closest')}

# Dashboard calling the Fertility and Employment Rate correlation graph.
@app.callback(Output('graph4','figure'),[Input('region-picker','value')])
#This code takes in the fertility data and plot it against the employment data to show the correlation.
def update_figure4(picked_region):
    sorted_df= df[df['Region']==picked_region]
    data=[]
    for year in sorted_df['Year'].unique():
        df_by_year = sorted_df[sorted_df['Year']== year]
        data.append(go.Scatter(x=df_by_year['Fertility Rate'], y= df_by_year['Employment Rate'], mode = 'markers+lines',
        opacity = 0.7, marker= {'size':15}, name=picked_region, showlegend= False))
   
    return {'data':data,'layout': go.Layout(title= 'Female Employment & Fertility', xaxis={'title':'Fertility Rate '+' '+ picked_region,
                'type': 'log'},yaxis={'title':'Employment Rate '+' '+ picked_region})}

#Dashboard calling the Fertility and Unemployment Rate correlation graph.
@app.callback(Output('graph5','figure'),[Input('region-picker','value')])   
#This code takes in the fertility data and plot it against the unemployment data to show the correlation.
def update_figure5(picked_region):
    sorted_df= df[df['Region']==picked_region]
    data=[]
    for year in sorted_df['Year'].unique():
        df_by_year = sorted_df[sorted_df['Year']==year]
        data.append(go.Scatter(x=df_by_year['Fertility Rate'], y= df_by_year['Unemployment Rate'], mode = 'markers+lines',
        opacity = 0.7, marker= {'size':15}, name= picked_region, showlegend= False))
      
    return {'data':data,'layout': go.Layout(title= 'Female Unemployment & Fertility', xaxis={'title':'Fertility Rate '+' '+ picked_region,
                'type': 'log'},yaxis={'title':'Unemployment Rate '+' '+picked_region})}



if __name__ =='__main__':
    app.run_server(debug=True)

    