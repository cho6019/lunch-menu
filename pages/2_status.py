import pandas as pd
import streamlit as st
from lunch_menu.db import select_table
import matplotlib.pyplot as plt

st.set_page_config(page_title='STATUS')

st.markdown("# Demo")
st.sidebar.header("Plotting Demo")

st.subheader("확인")
select_df = select_table()
select_df

st.subheader("통계")

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
