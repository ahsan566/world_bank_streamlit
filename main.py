import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import wbdata as wb
import datetime as dt

st.title('Analysis of infant deaths around the world')
st.header('World Development Indicators')
# st.text('_______________________________________________________')
'''
___
'''

@st.cache
def load_wb_data():
    indicator = 'SH.DTH.IMRT'
    start_date = 2000
    end_date = 2015
    data_dates = (dt.datetime(start_date,1,1), dt.datetime(end_date,1,1))
    data = wb.get_dataframe({indicator:'values'},
                           country=('PAK','IND','SAU'),
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
    df2['geometry'].plot()
    plt.title("World Map")
    plt.axis('off')
    st.pyplot(plt)

st.sidebar.text("")
st.sidebar.text("")

countries = st.multiselect(
    'Select countries',
    df['country'].unique()
)

st.write("you selected", countries)

st.sidebar.text("")
st.sidebar.text("")

# if division:
#     l = list(df[df['division']==division]['district'])
#     district = st.sidebar.selectbox(
#         'Select a district',
#         [x.title() for x in l]
#     )
#
# district = district.lower()
#
# df[df['district'].str.contains(district)]['geometry'].plot(color='#FB5455')
# plt.title(district.title())
# # plt.figure(figsize=(30,20))
# plt.axis('off')
# st.pyplot(plt)
#
#
# st.subheader(district.title())
# value = df[df['district']==district].index
# val = df.loc[value]
# x = val.drop('geometry', axis=1)
# st.table(x.T.squeeze())

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
