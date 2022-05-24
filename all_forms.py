import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time
import requests
import re


st.set_page_config(page_title="Amazon All Forms", page_icon="⚕️​", layout="wide")
alt.renderers.set_embed_options(actions=False)
#st.markdown("<h1 style='text-align: center; color: red;'>Tablets Report</h1>", unsafe_allow_html=True)

#st.markdown("<p style='text-align: center; color: black;'>This interactive report is created as an example of explatory sales data analysis report for Amazon's Categories.</p>", unsafe_allow_html=True)

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

url = 'https://raw.githubusercontent.com/ngolos/ns-streamlit/main/may_apr.csv'

@st.cache
def get_data(url):

    #df = pd.read_csv(url_csv, keep_default_na=False)
    #df=pd.read_csv(url, keep_default_na=False)
    #'C:/Users/nago/Desktop/vizualization/nutrastar/health_Bestsellers_db/may_jan.csv'
    df = pd.read_csv(url, keep_default_na=False)

    return df

df1=get_data('https://raw.githubusercontent.com/ngolos/ns-streamlit/main/may_feb.csv')
df_ingr_form=get_data('https://raw.githubusercontent.com/ngolos/ns-streamlit/main/split_by_ingr_form.csv')


st.title('All Delivery Forms Report')
"""
- Part 1: Overall view - Sales by Delivery Form, Top Brands.
- Part 2: Top Ingredients
- Part 3: View By Functionality
- All the data is based on May'21 - Apr'22 Amazon Best Sellers Rankings in Dietaty Supplements Category. Fluid Forms are excluded (drops, oils, liquids).
"""
st.write("---")
# Filters
#month_list
month=['apr','mar','feb', 'jan', "dec", 'nov', 'oct', 'sep', 'aug', 'jul', 'jun', 'may']

product_forms=["Capsules", 'Gummy', 'Powder', 'Softgels', 'Tablets']


function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Stress_Sleep','Weight_Mngm' ]
st.header(' Sales by Delivery Form, Top Brands')
col01, col02, col03, col04, col05, col06 = st.columns([3,1,3,1,3,1])
with col01:
    form_choice = st.selectbox('Select delivery form:', product_forms)

with col03:
    month_choice = st.selectbox('Select month:', month)
pattern=f"Mo_Revenue_{month_choice}"
#st.dataframe(tablets_all)
#st.header(f"{form_choice} Overall Sales Revenue: {month_choice}'21 Monthly Sales Est:$ {Rev_All} Mln")


#st.dataframe(df1)
source=df1[df1['Type']==form_choice].groupby(['Brand'], as_index=False)[pattern].sum().sort_values(by=pattern, ascending=False).head(15)
new=source[pattern].div(1000000).round(1)
source['Mo_Revenue_mln']=new

color_dict={"Gummy":"lightseagreen", "Capsules":"navy",  "Powder":"silver", "Softgels":"lightslategray", "Tablets":"royalblue"}

chart=alt.Chart(source).mark_bar(color=color_dict[form_choice]).encode(
    x=alt.X('Mo_Revenue_mln:Q', axis=alt.Axis(title='Monthly Revenue, mln$', tickMinStep=1)),
    y=alt.Y('Brand', sort="-x", title=" "),
).properties(height=300, width=350)

text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='Mo_Revenue_mln:Q'
).properties(
    title=f"{form_choice}: Top 15 Brands in {month_choice}"
)
top_15brands=(chart+text)
cols=['Mo_Revenue_may', 'Mo_Revenue_jun', 'Mo_Revenue_jul', 'Mo_Revenue_aug',
   'Mo_Revenue_sep', 'Mo_Revenue_oct', 'Mo_Revenue_nov', 'Mo_Revenue_dec',
   'Mo_Revenue_jan', 'Mo_Revenue_feb', 'Mo_Revenue_mar', 'Mo_Revenue_apr']
source_by_type=df1.groupby('Type')[cols].sum().unstack().reset_index()
source_by_type.columns=['month', 'Type', 'sales_mln']
source_by_type.month=source_by_type.month.str.replace('Mo_Revenue_', "")
source_by_type['sales_mln']=(source_by_type['sales_mln']/1000000).round(1)

months=['may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr']
sales_by_form=alt.Chart(source_by_type[source_by_type['Type']==form_choice]).mark_area(point=True).encode(
    x=alt.X('month', sort=months, title=""),
    y=alt.Y('sales_mln', title='Revenue, mln$'),
    color=alt.Color('Type:N', legend=None, scale=alt.Scale(
        domain=['Gummy', 'Capsules', "Powder", "Softgels", "Tablets"],
        range=["lightseagreen", 'navy', "silver", "lightslategray", "royalblue"])),
    #column=alt.Column("Type", title=""),
    tooltip=['sales_mln']
).properties(
    title=f"{form_choice}: Sales Revenue, mln$"
)



col101, col102, col103, col104= st.columns([3,1,3,3])

with col101:
    st.altair_chart(sales_by_form, use_container_width=True)
with col103:
    st.altair_chart(top_15brands, use_container_width=True)
with col104:
    st.dataframe(source.loc[:,['Brand', "Mo_Revenue_mln"]].reset_index(drop=True))

st.write("---")
st.header(f'{month_choice}: Revenue $Mln Top 15 Ingredients in {form_choice}')
st.dataframe(df_ingr_form.loc[(df_ingr_form.form==form_choice) & (df_ingr_form['month']==month_choice)].nlargest(15, 'revenue'))
