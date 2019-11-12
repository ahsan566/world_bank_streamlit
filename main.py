import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import wbdata as wb
import datetime as dt
import seaborn as sns
import cufflinks as cf
import plotly
import plotly.offline as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

SMALL_SIZE = 8
MEDIUM_SIZE = 12
BIGGER_SIZE = 17

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# "---------------------------------------------------------------------------------------"

st.title('Analysis of Infant deaths around the world')
st.subheader('World Bank Data')
st.write("Analysis of infant mortality rate around the world using world bank api.")
# st.text('_______________________________________________________')
# '''
# ___
# '''

@st.cache
def load_wb_data():
    indicator = 'SH.DTH.IMRT'
    start_date = 2010
    end_date = 2015
    data_dates = (dt.datetime(start_date,1,1), dt.datetime(end_date,1,1))
    data = wb.get_dataframe({indicator:'values'},
                           country=('PAK','IND'),
                           data_date = data_dates,
                           convert_date=False,
                           keep_levels=True)
    data = data.reset_index()
    return data

@st.cache
def load_countries_coordinates():
    data = gpd.read_file('world_countries.json')
    return data


# data_load = st.text("Loading data...")
df = load_wb_data()
df2 = load_countries_coordinates()
# data_load.text("Loading data... done!")

def get_country_indicator(country, indicator, start, end):
    data_dates = (dt.datetime(start,1,1), dt.datetime(end,1,1))
    data = wb.get_dataframe({indicator:'indicator'},
                       country=country,
                       data_date = data_dates,
                       convert_date=False,
                       keep_levels=True)
    data = data.reset_index()
    return data['indicator']


def plot_data(indicator, countries, start=2000, end=2015):
    ind = wb.get_indicator(indicator, display=False)

    title = ind[0]['name']

    new_df = pd.DataFrame()
    for country in countries:
        new_df = new_df.append(df2[df2['id']==country])
    new_df['geometry'].plot(figsize=(20,10))
    plt.axis('off')
    st.pyplot(plt)

    # Create a plotly figure
    colors = ['#F4652A', '#2E86C1', '#82427B', '#3A924C', '#34495E']
    trace_list = []
    layout = go.Layout(title = title,
                       hovermode = 'closest',
                       # paper_bgcolor = "rgba(0,0,0,0)"
                       plot_bgcolor =  "white",
                       xaxis = {'title':'',
                                'showgrid':True
                                },
                       yaxis = {'title':'deaths',
                                'showgrid':True,}
                       )

    for country, color in zip(countries, colors):
        trace = go.Scatter(x = [i for i in range(start,end+1)], y = get_country_indicator(country,indicator,start,end),
                            # fill = 'tozeroy',
                            # fillcolor = '#93BAFC',
                            name = country,
                            line = dict(width = 2, color = color),
                            )
        trace_list.append(trace)

    fig = go.Figure(data = trace_list, layout = layout)
    fig.update_xaxes(showline=True, ticks='outside', tickmode='linear', tick0=1, dtick=2, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, ticks='outside', tickmode='linear', tick0=500000, dtick=250000, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(
        legend=go.layout.Legend(
            # x=0,
            # y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="white",
            bordercolor="Black",
            borderwidth=1
        ),
        # title=go.layout.Title(xanchor='center')
    )
    st.plotly_chart(fig, width=0, height=0, sharing='streamlit')

def plot_data_subplots(countries, start=2000, end=2015):

    female_indicator = 'SP.DYN.IMRT.FE.IN'
    male_indicator = 'SP.DYN.IMRT.MA.IN'
    # Create a plotly figure
    colors = ['#F4652A', '#2E86C1', '#82427B', '#3A924C', '#34495E']
    trace_list = []
    layout = go.Layout(title = "",
                       hovermode = 'closest',
                       # paper_bgcolor = "rgba(0,0,0,0)"
                       plot_bgcolor =  "white",
                       xaxis = {'title':'',
                                'showgrid':True
                                },
                       yaxis = {'title':'deaths',
                                'showgrid':True,}
                       )

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Male", "Female"))

    fig.update_layout(title_text="Infant Mortality per 1000 births",
                      plot_bgcolor='white',
                      showlegend=False
                     )

    # For Male
    for country, color in zip(countries, colors):
        fig.add_trace(
            go.Scatter(x = [i for i in range(start,end+1)], y = get_country_indicator(country, male_indicator, start, end),
                            name = country,
                            line = dict(width = 2, color = color),
                       ),
            row=1, col=1
        )

    # For Female
    for country, color in zip(countries, colors):
        fig.add_trace(
            go.Scatter(x = [i for i in range(start,end+1)], y = get_country_indicator(country, female_indicator, start, end),
                            name = country,
                            line = dict(width = 2, color = color),
                       ),
            row=1, col=2
        )

    fig.update_xaxes(showline=True, showgrid=False, gridcolor='grey', ticks='outside', tickmode='linear', tick0=1, dtick=3, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, showgrid=False, gridcolor='grey', ticks='outside', nticks=8, linewidth=1, linecolor='black', mirror=True)

    st.plotly_chart(fig, width=0, height=0, sharing='streamlit')


st.sidebar.text("Created by: Ahsan Fayyaz")
st.sidebar.text("")
st.sidebar.title('Options')

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")

if st.sidebar.checkbox('Show wb data'):
    st.subheader("Raw data")
    st.write(df)

st.sidebar.text("")

if st.sidebar.checkbox('Show World map'):
    df2['geometry'].plot(color='#FB5455')
    plt.suptitle("World map")
    plt.axis('off')
    st.pyplot(plt)

st.sidebar.text("")
st.sidebar.text("")

countries = st.sidebar.multiselect(
    'Select countries',
    list(df2['name']),
    # default=[df2[df2['name']=="Pakistan"].iloc[0]['name']],
    ["Pakistan","India"],
)

li = []
if countries:
    for country in countries:
        c = df2[df2['name']==country]['id'].to_string(index=False)
        c = c.strip()
        li.append(c)

indicator = 'SH.DTH.IMRT'
# st.write("you selected", countries)
if countries:
    plot_data(indicator, li, 2001, 2016)
    plot_data_subplots(li, 2001, 2015)

st.sidebar.text("")
