import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st 

st.title('Find Out Rental Trends In Your Locality: Hyderabad')

st.markdown("""
* Select your locality from the dropdown menu on the left.
""")


df = pd.read_csv('merged_rental_hyderabad.csv')
df = df.loc[df['loc_count']>=20]
loc_list = list(df['locality'].unique())


prop_grp = df.groupby('property_type')
prop_rents = prop_grp['price'].mean()
prop_rents = dict(prop_rents)
list1 = prop_rents.keys()
list2 = prop_rents.values()
proprents_df = pd.DataFrame(list(zip(list1,list2)), columns=['property_type','mean_rent'])
proprents_df['mean_rent'] = proprents_df['mean_rent'].astype(int)

fig = px.bar(proprents_df,x='property_type', y='mean_rent', text='mean_rent',
            labels={'mean_rent':'Average Rent'}, color='mean_rent', color_continuous_scale = 'viridis') 

fig.update_traces(textposition='outside')
fig.update_layout(title_text="<b>Average Rents (by Property Type)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.47,
                 title_y=0.95,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig.update_xaxes(
        color='teal',
        title_text='Property Type',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True)

fig.update_yaxes(
        color='Teal',
        title_text='Average Rent (INR)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        tickfont_family='Arial',
        nticks = 20,
        gridcolor='lightblue',
        linecolor='red',
        linewidth=3,
        mirror = True)

fig.show()