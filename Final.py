

import pandas as pd
import dash
import dash_html_components as html
import webbrowser
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.SKETCHY])

def load_data():
    global df
    df=pd.read_csv('Global_Terror.csv')
    df.natlty1_txt=df.natlty1_txt.astype(str)
    
    global dfindia
    dfindia=pd.read_csv('India_Terror.csv')
    
    month={
        'January':1,
        'February':2,
        'March':3,
        'April':4,
        'May':5,
        'June':6,
        'July':7,
        'August':8,
        'September':9,
        'October':10,
        'November':11,
        'December':12
        }
    global month_list
    month_list=[{"label":key,"value":values} for key,values in month.items()]
    
    global date_list
    date_list= [{'label':x,'value':x} for x in range(1,32)]
    
    global temp_list1
    temp_list1=sorted(df['region_txt'].unique().tolist())
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in temp_list1]
    
    global temp_list
    temp_list=sorted(df['country_txt'].unique().tolist())
    global country_list
    country_list=[{'label':str(i),'value':str(i)} for i in temp_list]
    #will create a list of dictionaries
    
    #temp_list2=sorted(df['provstate'].unique().tolist()) here sorted will generate error due to presence of null state values
    temp_list2=df['provstate'].unique().tolist()
    global state_list
    state_list=[{'label':str(i),'value':str(i)} for i in temp_list2]
    
    #temp_list3=sorted(df['city'].unique().tolist())
    temp_list3=(df['city'].unique().tolist())
    global city_list
    city_list=[{'label':str(i),'value':str(i)} for i in temp_list3]
    
    temp_list4=sorted(df['attacktype1_txt'].unique().tolist())
    global attack_list
    attack_list=[{'label':str(i),'value':str(i)} for i in temp_list4]
    
    temp_list5={'Terrorist Organisation':'gname','Target Type':'targtype1_txt',
                'Target Nationality':'natlty1_txt','Type of Attack':'attacktype1_txt',
                'Weapon Type':'weaptype1_txt','Region':'region_txt',
                'Country Attacked':'country_txt'}
    global chart_list
    chart_list=[{'label':key,'value':values} for key,values in temp_list5.items()]
    
    #slider needs data in dictionary format
    global year_list
    global year_dict
    year_list=sorted(df['iyear'].unique().tolist())
    year_dict={str(year):str(year) for year in year_list}

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')    
    
def create_app_ui():
    main_layout=html.Div(
        [   
            #html.Img(src=app.get_asset_url('shutterstock_499799137_resize.jpg')),
            #style={"background-image": 'url("/assets/Background.PNG")'}
            html.H1(id='Main_title', children='TERRORISM ANALYSIS WITH INSIGHTS',style={'textAlign':'center','color':'white',
                    "background-image": 'url("/assets/shutterstock_499799137_resize.jpg")','background-position':'right top',
                    "background-size":'300px 70px'}),
            dcc.Tabs(id='main-tab',value='tab-1',children=[
                dcc.Tab(label='MAP TOOL',id='map-tool',value='tab-1',children=
                        [
                            dcc.Tabs(id='sub-tab1',value='tab-1',children=[
                                dcc.Tab(label='WORLD MAP TOOL',id='world-map-tool',value='tab-1', loading_state=True, children=[html.Div([
                                    dbc.Row([
                                    dbc.Col(dcc.Dropdown(id='month',options=month_list,
                                                 placeholder='Select Month',multi= True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='date',options=date_list,
                                                 placeholder='Select Day',multi=True),
                                                  width={'size':4,'offset':0,'order':1},),
                                    dbc.Col(dcc.Dropdown(id='region-dropdown',options=region_list,
                                                 placeholder='Select Region',multi= True),
                                                  width={'size':4,'offset':0,'order':1},),
                                    dbc.Col(dcc.Dropdown(id='country-dropdown',options=country_list,
                                                 placeholder='Select Country',multi= True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='state-dropdown',options=state_list,
                                                 placeholder='Select State',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    
                                    dbc.Col(dcc.Dropdown(id='city-dropdown',options=city_list,
                                                 placeholder='Select City',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='attack-dropdown',options=attack_list,
                                                 placeholder='Select Attack Type',multi=True),
                                                 width={'size':4,'offset':0,'order':1})
                                      ]),
                                    html.H5(id='year-title',children='Select year range'),
                                    dcc.RangeSlider(
                                        id='year-slider',
                                        min=min(year_list),
                                        max=max(year_list),
                                        value=[min(year_list),max(year_list)],
                                        marks=year_dict),
                                    html.Br(),
                                    html.H3(id='info',children=None),
                                    dcc.Graph(id='graph-object')
                                    ])]),
                                dcc.Tab(label='INDIA MAP TOOL',id='india-map-tool',value='tab-1a',children=[
                                    dbc.Row([
                                    dbc.Col(dcc.Dropdown(id='month1',options=month_list,
                                                 placeholder='Select Month',multi= True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='date1',options=date_list,
                                                 placeholder='Select Day',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='region-dropdown1',options=region_list,
                                                 value='South Asia',disabled=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='country-dropdown1',options=country_list,
                                                 value='India',disabled=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='state-dropdown1',options=state_list,
                                                 placeholder='Select State',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='city-dropdown1',options=city_list,
                                                 placeholder='Select City',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                    dbc.Col(dcc.Dropdown(id='attack-dropdown1',options=attack_list,
                                                 placeholder='Select Attack Type',multi=True),
                                                 width={'size':4,'offset':0,'order':1}),
                                                 ]),
                                    html.H5(id='year-title1',children='Select year range'),
                                    dcc.RangeSlider(
                                        id='year-slider1',
                                        min=min(year_list),
                                        max=max(year_list),
                                        value=[min(year_list),max(year_list)],
                                        marks=year_dict),
                                    html.Br(),
                                    html.H3(id='info1',children=None),
                                    dcc.Graph(id='graph-object1')
                                    ])
                                ])
                            ]),
                dcc.Tab(label='CHART TOOL',id='chart-tool',value='chart-1',children=
                        [
                            dcc.Tabs(id='sub-tab2',value='chart-1',children=[
                                dcc.Tab(label='WORLD CHART TOOL',id='world-chart-tool',value='chart-1',children=[
                                    dcc.Dropdown(id='chart-dropdown',options=chart_list,value = 'region_txt'
                                                 ),
                                    html.Hr(),
                                    html.H4(id='text',children= "Please type your filter search below and press Enter"),
                                    html.Br(),
                                    dcc.Input(id='filter',type='search',placeholder='Search Filter',
                                              debounce=True),
                                    html.Hr(),
                                    dcc.Graph(id='graph-object2')
                                    ]),
                                dcc.Tab(label='INDIA CHART TOOL',id='india-chart-tool',value='chart-1b',children=[
                                    dcc.Dropdown(id='chart-dropdown1',options=chart_list, value='region_txt'
                                                 ),
                                    html.Hr(),
                                    html.H4(id='text1',children= "Please type your filter search below and press Enter"),
                                    html.Br(),
                                    dcc.Input(id='filter1',type='search',placeholder='Search Filter',
                                              debounce=True),
                                    html.Hr(),
                                    dcc.Graph(id='graph-object3')
                                    ]),
                                
                                ])
                            ])
            ])
            
            ]
        )
    
    return main_layout

@app.callback(
    Output('graph-object2','figure'),
    [
     Input('chart-dropdown','value'),
     Input('filter','value')
     ]
    )

def update_chart(dd_value,input_value):
    print("Datatype of input_value=",str(type(input_value)))
    print("Value of input_value is=",str(input_value))
    
    global figure
    figure=None
    figure=go.Figure()
    if dd_value!=None:
        newlist=df[dd_value].unique().tolist()
        if input_value!=None: 
            i1=[] 
            for i in newlist:
                if input_value in i.lower():
                    i1.append(i)
            input_value=i1
        elif input_value==None or input_value==' ' or len(input_value)==0:
            input_value=newlist
        else:
            pass
        for i in input_value:
            df1=df[df[dd_value]==i]
            df2=df1['iyear'].value_counts().rename_axis('year').reset_index(name='counts')
            df2.sort_values(by=['year'],inplace=True) 
            figure=figure.add_trace(go.Scatter(name=i,x=df2['year'],y=df2['counts'],mode='lines',stackgroup='one'))
            figure.update_layout(showlegend=True
                )
    
    else:
        pass
    
    return figure

@app.callback(
    Output('graph-object3','figure'),
    [
     Input('chart-dropdown1','value'),
     Input('filter1','value')
     ]
    )

def update_chart1(dd_value,input_value):
    print("Datatype of input_value=",str(type(input_value)))
    print("Value of input_value is=",str(input_value))
    
    global figure
    figure=None
    figure=go.Figure()
    if dd_value!=None:
        newlist=dfindia[dd_value].unique().tolist()
        if input_value!=None: 
            i1=[] 
            for i in newlist:
                if input_value in i.lower():
                    i1.append(i)
            input_value=i1
        elif input_value==None or input_value==' ' or len(input_value)==0:
            input_value=newlist
        else:
            pass
        for i in input_value:
            df1=dfindia[dfindia[dd_value]==i]
            df2=df1['iyear'].value_counts().rename_axis('year').reset_index(name='counts')
            df2.sort_values(by=['year'],inplace=True) 
            figure=figure.add_trace(go.Scatter(name=i,x=df2['year'],y=df2['counts'],mode='lines',stackgroup='one'))
            figure.update_layout(showlegend=True)

    else:
        pass
    
    return figure

@app.callback(
    Output('date','options'),
    [
     Input('month','value')
     
     ]
    )
def update_date(month_value):
    date_list= [x for x in range(1,32)]
    
    if month_value==None:
        return []
    elif len(month_value)==1:
        if month_value[0] in [1,3,5,7,8,10,12]:
            return [{'label':m,'value':m} for m in date_list]
        elif month_value[0] in [4,6,9,11]:
            return [{'label':m,'value':m} for m in date_list[:-1]] #start from beginning end at one value before
        elif month_value[0]==2:
            return [{'label':m,'value':m} for m in date_list[:-2]]
        else:
            return []
    else:
        day31=0
        day30=0
        day29=0
        for i in month_value:
            if i in [1,3,5,6,7,8,10,12]:
                day31=day31+1
            elif i in [4,7,9,11]:
                day30=day30+1
            elif i==2:
                day29=day29+1
            else:
                pass
            
        if day31!=0:
            return [{'label':m,'value':m} for m in date_list]
        elif day31==0 and day30!=0:
            return [{'label':m,'value':m} for m in date_list[:-1]]
        else:
            return []
            
@app.callback(
    Output('country-dropdown','options'),
    [
     Input('region-dropdown','value')
     ]
    )
def update_country(region_value):
    if region_value!= None:
        return[{'label':str(i),'value':str(i)} for i in df[df['region_txt'].isin(region_value)] ['country_txt'].unique().tolist()]
    else:
        return []
    
@app.callback(
    Output('state-dropdown','options'),
    [
     Input('country-dropdown','value')
     ]
    )
def update_state(country_value):
    if country_value!=None:
        return[{'label':str(i),'value':str(i)} for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist()]
    else:
        return []
    
@app.callback(
    Output('city-dropdown','options'),
    [
     Input('state-dropdown','value')
     ]
    )
def update_city(state_value):
    if state_value!=None:
        return[{'label':str(i),'value':str(i)} for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist()]
    else:
        return []

@app.callback([
    dash.dependencies.Output('graph-object','figure'),
    dash.dependencies.Output('info','children')],
    [
     dash.dependencies.Input('month','value'),
     dash.dependencies.Input('date','value'),
     dash.dependencies.Input('region-dropdown','value'),
     dash.dependencies.Input('country-dropdown','value'),
     dash.dependencies.Input('state-dropdown','value'),
     dash.dependencies.Input('city-dropdown','value'),
     dash.dependencies.Input('attack-dropdown','value'),
     dash.dependencies.Input('year-slider','value'),
     ]
    )

def update_app_ui(month_value,date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
    
    print("Datatype of month_value=",str(type(month_value)))
    print("Value of month_value is=",str(month_value))
    
    print("Datatype of date_value=",str(type(date_value)))
    print("Value of date_value is=",str(date_value))
    
    print("Datatype of region_value=",str(type(region_value)))
    print("Value of region_value is=",str(region_value))
    
    print("Datatype of country_value=",str(type(country_value)))
    print("Value of country_value is=",str(country_value))
    
    print("Datatype of state_value=",str(type(state_value)))
    print("Value of state_value is=",str(state_value))
    
    print("Datatype of city_value=",str(type(city_value)))
    print("Value of city_value is=",str(city_value))
    
    print("Datatype of attack_value=",str(type(attack_value)))
    print("Value of attack_value is=",str(attack_value))
    
    print("Datatype of year_value=",str(type(year_value)))
    print("Value of year_value is=",str(year_value))
    
    df=pd.read_csv('Global_Terror.csv')
    
    global figure
    figure=go.Figure() #creates blank figure
    
    year_values=range(year_value[0],year_value[1]+1)
    dfa=df[df['iyear'].isin(year_values)]
    children=None
    
    if (month_value== None or month_value== []) and (date_value== None or date_value== []):
        pass
    
    elif (month_value==None or month_value==[]) and date_value!= None:
        dfa=dfa[dfa['iday'].isin(date_value)]
        
    elif month_value!=None and (date_value==None or date_value==[]):
        dfa=dfa[dfa['imonth'].isin(month_value)]
        
    else:
        dfa=dfa[(dfa['imonth'].isin(month_value)) & (dfa['iday'].isin(date_value))]
        
    
    if (region_value== None or region_value==[]):
        pass
        
    elif region_value!= None and (country_value==None or country_value==[]):
        dfa=dfa[dfa['region_txt'].isin(region_value)]
    
    elif country_value!=None and (state_value==None or state_value==[]):
        dfa=dfa[dfa['region_txt'].isin(region_value)]
        dfa=dfa[dfa['country_txt'].isin(country_value)]
        
    elif state_value!=None and (city_value==None or city_value==[]):
        dfa=dfa[dfa['region_txt'].isin(region_value)]
        dfa=dfa[dfa['country_txt'].isin(country_value)]
        dfa=dfa[dfa['provstate'].isin(state_value)]
        
    elif city_value!= None:
        dfa=dfa[dfa['region_txt'].isin(region_value)]
        dfa=dfa[dfa['country_txt'].isin(country_value)]
        dfa=dfa[dfa['provstate'].isin(state_value)]
        dfa=dfa[dfa['city'].isin(city_value)]
        
    else:
        pass

    if (attack_value== None or attack_value==[]):
       pass
   
    else:
        dfa=dfa[dfa['attacktype1_txt'].isin(attack_value)]
        
    if len(dfa.index)==0:
        dfa = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        dfa.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
        children='No records avaiable'
    else:
        pass
        
    figure=px.scatter_mapbox(dfa,lat='latitude',lon='longitude',
                                 color='attacktype1_txt',
                                 hover_data=['region_txt','country_txt','provstate','city','attacktype1_txt','nkill','iyear','iday','imonth'],
                                 zoom=1) 
    figure.update_layout(mapbox_style='open-street-map',autosize=True,margin=dict(l=0,r=0,t=25,b=20))
    
    return figure,children

'''
The code below is for India map tool
'''
@app.callback(
    Output('date1','options'),
    [
     Input('month1','value')
     
     ]
    )
def update_date1(month_value):
    date_list= [x for x in range(1,32)]
    
    if month_value==None:
        return []
    elif len(month_value)==1:
        if month_value[0] in [1,3,5,6,8,10,12]:
            return [{'label':m,'value':m} for m in date_list]
        elif month_value[0] in [4,7,9,11]:
            return [{'label':m,'value':m} for m in date_list[:-1]] #start from beginning end at one value before
        elif month_value[0]==2:
            return [{'label':m,'value':m} for m in date_list[:-2]]
        else:
            return []
    else:
        day31=0
        day30=0
        day29=0
        for i in month_value:
            if i in [1,3,5,6,7,8,10,12]:
                day31=day31+1
            elif i in [4,7,9,11]:
                day30=day30+1
            elif i==2:
                day29=day29+1
            else:
                pass
            
        if day31!=0:
            return [{'label':m,'value':m} for m in date_list]
        elif day31==0 and day30!=0:
            return [{'label':m,'value':m} for m in date_list[:-1]]
        else:
            return []
    
@app.callback(
    Output('state-dropdown1','options'),
    [
     Input('country-dropdown1','value')
     ]
    )
def update_state1(country_value):
    if country_value!=None:
        return[{'label':str(i),'value':str(i)} for i in df[df['country_txt']==country_value] ['provstate'].unique().tolist()]
    else:
        return []
    
    
@app.callback(
    Output('city-dropdown1','options'),
    [
     Input('state-dropdown1','value')
     ]
    )
def update_city1(state_value):
    if state_value!=None:
        return[{'label':str(i),'value':str(i)} for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist()]
    else:
        return []


@app.callback([
    dash.dependencies.Output('graph-object1','figure'),
    dash.dependencies.Output('info1','children')
    ],
    [
     dash.dependencies.Input('month1','value'),
     dash.dependencies.Input('date1','value'),
     dash.dependencies.Input('region-dropdown1','value'),
     dash.dependencies.Input('country-dropdown1','value'),
     dash.dependencies.Input('state-dropdown1','value'),
     dash.dependencies.Input('city-dropdown1','value'),
     dash.dependencies.Input('attack-dropdown1','value'),
     dash.dependencies.Input('year-slider1','value'),
     ]
    )

def update_app_ui1(month_value,date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
    
    print("Datatype of month_value=",str(type(month_value)))
    print("Value of month_value is=",str(month_value))
    
    print("Datatype of date_value=",str(type(date_value)))
    print("Value of date_value is=",str(date_value))
    
    print("Datatype of region_value=",str(type(region_value)))
    print("Value of region_value is=",str(region_value))
    
    print("Datatype of country_value=",str(type(country_value)))
    print("Value of country_value is=",str(country_value))
    
    print("Datatype of state_value=",str(type(state_value)))
    print("Value of state_value is=",str(state_value))
    
    print("Datatype of city_value=",str(type(city_value)))
    print("Value of city_value is=",str(city_value))
    
    print("Datatype of attack_value=",str(type(attack_value)))
    print("Value of attack_value is=",str(attack_value))
    
    print("Datatype of year_value=",str(type(year_value)))
    print("Value of year_value is=",str(year_value))
    
    df=pd.read_csv('Global_Terror.csv')
    
    global figure
    figure=go.Figure() #creates blank figure
    children=None
    
    year_values=range(year_value[0],year_value[1]+1)
    dfa=df[df['iyear'].isin(year_values)]
    
    if (month_value== None or month_value== []) and (date_value== None or date_value== []):
        pass
    
    elif (month_value==None or month_value==[]) and date_value!= None:
        dfa=dfa[dfa['iday'].isin(date_value)]
        
    elif month_value!=None and (date_value==None or date_value==[]):
        dfa=dfa[dfa['imonth'].isin(month_value)]
        
    else:
        dfa=dfa[(dfa['imonth'].isin(month_value)) & (dfa['iday'].isin(date_value))]
        
    
    if country_value!=None and (state_value==None or state_value==[]):
        dfa=dfa[dfa['region_txt']==region_value]
        dfa=dfa[dfa['country_txt']==country_value]
        
    
    elif state_value!=None and (city_value==None or city_value==[]):
        dfa=dfa[dfa['region_txt']==region_value]
        dfa=dfa[dfa['country_txt']==country_value]
        dfa=dfa[dfa['provstate'].isin(state_value)]
        
    elif city_value!= None:
        dfa=dfa[dfa['region_txt']==region_value]
        dfa=dfa[dfa['country_txt']==country_value]
        dfa=dfa[dfa['provstate'].isin(state_value)]
        dfa=dfa[dfa['city'].isin(city_value)]
        
    else:
        pass

    if (attack_value== None or attack_value==[]):
       pass
   
    else:
        dfa=dfa[dfa['attacktype1_txt'].isin(attack_value)]
        
    if len(dfa.index)==0:
        dfa = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        dfa.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
        children='No records avaiable'
    else:
        pass
        
    figure=px.scatter_mapbox(dfa,
    lat='latitude',
    lon='longitude',
    color='attacktype1_txt',
    hover_data=['region_txt','country_txt','provstate','city','attacktype1_txt','nkill','iyear','iday','imonth'],
    zoom=3
    ) 
    figure.update_layout(mapbox_style='open-street-map',autosize=True,margin=dict(l=0,r=0,t=25,b=20))
    
    return figure,children

def main():
    print('Welcome!')
    
    load_data()
    
    open_browser()
    
    global app
    app.layout=create_app_ui() 
    app.title= "Terrorism Analysis with insights"
    
   
    app.run_server(port=8050,host='127.0.0.1')
    
    
    print('Thank you!')
    
    app= None
    df= None
    
if __name__=='__main__':
    main()