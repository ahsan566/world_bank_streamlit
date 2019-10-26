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

"---------------------------------------------------------------------------------------"

st.title('Analysis of infant deaths around the world')
st.header('World Development Indicators')
# st.text('_______________________________________________________')
'''
___
'''

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
    return data[['indicator']]


def plot_data(indicator, countries, start=2000, end=2015):
    ind = wb.get_indicator(indicator, display=False)

    title = ind[0]['name']

    new_df = pd.DataFrame()
    for country in countries:
        new_df = new_df.append(df2[df2['id']==country])
    new_df['geometry'].plot(figsize=(20,10))
    plt.axis('off')
    st.pyplot(plt)

    fig, axis = plt.subplots(figsize=(10,5))
    sns.set_style('white')

    for country in countries:
        axis.plot(range(start,end+1), get_country_indicator(country,indicator,start,end), marker='o')
        axis.set_ylabel('deaths')
        axis.set_title(title)

    plt.legend(countries)
    # plt.figure(figsize=(10,20))
    plt.title = title
    plt.ylabel = "deaths"
    st.pyplot(plt)


st.sidebar.title('Options')

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")

if st.sidebar.checkbox('Show wb data'):
    st.subheader("Raw data")
    st.write(df)

if st.sidebar.checkbox('Show countries data'):
    st.subheader("Raw data")
    # df2 = pd.DataFrame(df2)
    st.write(df2)

st.sidebar.text("")

if st.sidebar.checkbox('Show full map'):
    df2['geometry'].plot(color='#FB5455')
    # plt.title("World Map")
    plt.axis('off')
    st.pyplot(plt)

st.sidebar.text("")
st.sidebar.text("")

countries = st.multiselect(
    'Select countries',
    df2['name'].unique(),
)

li = []
if countries:
    for country in countries:
        c = df2[df2['name']==country]['id'].to_string(index=False)
        c = c.strip()
        li.append(c)
    print("countries: ", li)

indicator = 'SH.DTH.IMRT'
# st.write("you selected", countries)
if countries:
    plot_data(indicator, li, 2001, 2016)

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("Created by: Ahsan Fayyaz")
