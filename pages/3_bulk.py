import streamlit as st
from lunch_menu.db import get_connection
import pandas as pd


st.set_page_config(page_title='BULK')

st.markdown("# Demo")
st.sidebar.header("Plotting Demo")

st.subheader("벌크 인서트")
importPress = st.button("한방에 인서트")

if importPress:
    conn = get_connection()
    cursor = conn.cursor()
    #cursor.execute("TRUNCATE TABLE lunch_menu;")
    for i in range(not_na_df.shape[0]):
        cursor.execute("INSERT INTO lunch_menu(menu_name, member_name, dt) VALUES (%s, %s, %s);",
        (not_na_df.iloc[i, 2], new_list.index(not_na_df.iloc[i, 0])+1, not_na_df.iloc[i, 1]))
    conn.commit()
    cursor.close()
    conn.close()
    st.write('DONE!')
