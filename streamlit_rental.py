import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st 

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Find Out Rental Trends In Your Desired Locality: Hyderabad')
st.markdown("""
* Select your locality from the dropdown menu on top left.
* Data freshly scraped from web during 3rd week of September 2021.
* [Github Repo](https://github.com/vijayv500/Hyderabad-Rental-Market-Analysis), [Twitter](https://twitter.com/vijayv500), [Medium Blog](https://vijayv500.medium.com).
* [Visit this link for more charts on Hyderabd rental market and the methodology adopted for analysis.](https://vijayv500.medium.com/mega-analysis-hyderabad-rental-market-in-charts-sep-2021-85f6b6a61c20)
* Please scroll down till the end.
""")


df = pd.read_csv('merged_rental_hyderabad.csv')
df = df.loc[df['loc_count']>=20.0]
df.sort_values(by='loc_count',ascending=False,inplace=True)
loc_list = list(df['locality'].unique())
chosen_loc = st.sidebar.selectbox('Locality',loc_list)
df = df.loc[(df['locality']==chosen_loc)]
st.header('Rental Trends in  '+ '"'+chosen_loc + '"'+":")

# *************** Average Rent by Property Type **********************************************************

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
                 title_y=0.93,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig.update_xaxes(
        color='teal',
        title_text='Property Type',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='royalblue',
        title_standoff = 15,
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True)

fig.update_yaxes(
        color='Teal',
        title_text='Average Rent (INR)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='royalblue',
        title_standoff = 15,
        tickfont_family='Arial',
        showgrid=False,
        nticks = 20,
        linecolor='red',
        linewidth=3,
        mirror = True)

fig.show()

st.plotly_chart(fig)

# ************************************ Median Rents: Apartments ********************************************* 

df1 = df.loc[df['bedrooms']==2.0]
fur_grp = df1.groupby('furnish_status')
fur_rents = fur_grp['price'].median()
fur_rents = dict(fur_rents)
fur_types2 = list(fur_rents.keys())
fur_values2 = list(fur_rents.values())
fur_values2 = [int(i) for i in fur_values2]

df2 = df.loc[df['bedrooms']==3.0]
fur_grp = df2.groupby('furnish_status')
fur_rents = fur_grp['price'].median()
fur_rents = dict(fur_rents)
fur_types3 = list(fur_rents.keys())
fur_values3 = list(fur_rents.values())
fur_values3 = [int(i) for i in fur_values3]

df3 = df.loc[df['bedrooms']==4.0]
fur_grp = df3.groupby('furnish_status')
fur_rents = fur_grp['price'].median()
fur_rents = dict(fur_rents)
fur_types4 = list(fur_rents.keys())
fur_values4 = list(fur_rents.values())
fur_values4 = [int(i) for i in fur_values4]

df4 = df.loc[df['bedrooms']==1.0]
fur_grp = df4.groupby('furnish_status')
fur_rents = fur_grp['price'].median()
fur_rents = dict(fur_rents)
fur_types1 = list(fur_rents.keys())
fur_values1 = list(fur_rents.values())
fur_values1 = [int(i) for i in fur_values1]

fig = go.Figure(data=[
    go.Bar(name='1 BHK', x=fur_types1, y=fur_values1,text=fur_values1),
    go.Bar(name='2 BHK', x=fur_types2, y=fur_values2,text=fur_values2),
    go.Bar(name='3 BHK', x=fur_types3, y=fur_values3,text=fur_values3),
    go.Bar(name='4 BHK', x=fur_types4, y=fur_values4,text=fur_values4)
])
fig.update_layout(barmode='group')

fig.update_traces(textposition='outside')


fig.update_layout(title_text="<b>Median Rents: Apartments (by Furnished Status)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.49,
                 title_y=0.85,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig.update_xaxes(
        color='teal',
        title_text='Property Type',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='royalblue',
        title_standoff = 15,
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True)

fig.update_yaxes(
        color='Teal',
        title_text='Median Rent (INR)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='royalblue',
        title_standoff = 15,
        showgrid = False,
        tickfont_family='Arial',
        linecolor='red',
        linewidth=3,
        mirror = True)
fig.show()

st.plotly_chart(fig)

# ************************* Monthly Trend: Average Rents ****************************************

try:
        df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')
        mean_list = []

        for i in range(7,10):
            filt = (df['date_posted'].dt.month==i)
            df_new = df.loc[filt]
            mean_list.append(df_new['price'].mean())

        mean_list = list(map(int,mean_list))    
        mean_names = ['July 2021', 'August 2021','September 2021']

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x= mean_names,
            y= mean_list,
            name='Average Rent Value',
            marker_color='orange',
            text=mean_list)
                     )

        fig.update_traces(textposition='outside')

        fig.update_layout(title_text="<b>Monthly Trend: Average Rents</b>",
                         title_font_size=25,
                         title_font_color='green',
                         title_font_family='Titillium Web',
                         title_x=0.5,
                         title_y=0.85,
                         title_xanchor='center',
                         title_yanchor='top'
                         )

        fig.update_xaxes(
                color='teal',
                title_text='Month',
                title_font_family='Open Sans',
                title_font_size=20,
                title_font_color='royalblue',
                title_standoff = 15,
                tickmode='auto',
                nticks=48,
                linecolor='red',
                linewidth=3,
                mirror=True)

        fig.update_yaxes(
                color='Teal',
                title_text='Average Rent (INR)',
                title_font_family='Droid Sans',
                title_font_size=20,
                title_font_color='royalblue',
                showgrid=False,
                title_standoff = 15,
                tickfont_family='Arial',
                linecolor='red',
                linewidth=3,
                mirror = True) 


        st.plotly_chart(fig)
except:
        print('404')        


# ****************************** wordcloud: builders *****************************************



df['builder'] = df['builder'].replace(np.nan,'',regex=True)
builder_list = df['builder'].values.tolist()

count = Counter(builder_list)
wordcloud = WordCloud(width = 1600, height = 800,background_color='black')\
.generate_from_frequencies(count)
plt.figure(figsize=(40,30))
plt.imshow(wordcloud)
plt.axis("off")
plt.show() 

st.markdown("""
        * Note: Some localities may display blank image(s) below if there is no data on builders/projects.
        * Bigger the font in the image, more the count of the builder/project in property listings.
        """)
st.header('Builders in  '+ '"'+chosen_loc + '"'+":")
st.pyplot()



# ******************************** wordcloud: projects ******************************************

df['project'] = df['project'].replace(np.nan,'',regex=True)
project_list = df['project'].values.tolist()

count = Counter(project_list)
wordcloud = WordCloud(width = 1600, height = 800,background_color='lightgreen')\
.generate_from_frequencies(count)
plt.figure(figsize=(40,30))
plt.imshow(wordcloud)
plt.axis("off")
plt.show() 

st.header('Projects in  '+ '"'+chosen_loc + '"'+":")
st.pyplot()
