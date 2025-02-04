import pandas as pd
import streamlit as st

df = pd.read_csv('menu.csv')

df_melt = df.drop(columns = ['gmail', 'github', 'domain', 'vercel', 'role'])
df_melt = df_melt.melt(id_vars=['ename'], var_name = 'dt', value_name = 'menu_name')
df_2 = df_melt
df_2 = df_2[~df_2['menu_name'].isin(['-', 'x', '<결석>'])]
df_2.dropna()

df_3 = df_2.groupby('ename').size().sort_values(ascending=False)

st.write("""
         ## 인원별 식사 횟수
         """)

st.write(df_3)
st.bar_chart(df_3)
