import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#from dotenv import load_dotenv
from lunch_menu.db import get_connection
from lunch_menu.db import insert_menu
from lunch_menu.db import select_table
from datetime import datetime

# dotenv가 .env의 정보를 환경변수화
#load_dotenv()

# page title
st.title("순신샵 점심 기록 현황")

# 필요정보 추출
df = pd.read_csv('note/menu.csv')
start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                     var_name='dt', value_name='menu')
not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
select_df = pd.DataFrame(not_na_df, columns=['menu','ename','dt'])
gdf = select_df.groupby('ename')['menu'].count().reset_index()
name_list = gdf['ename']


st.subheader("기록정보")
select_df = select_table()
select_df

st.subheader("기록횟수")

gdf = select_df.groupby('ename')['menu'].count().reset_index()
gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
try:
    fig, ax = plt.subplots()
    gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.write("not enough data")
    print(f"Exception{e}")


