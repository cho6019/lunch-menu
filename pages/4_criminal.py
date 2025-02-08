import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection, insert_menu, select_table
from datetime import datetime

st.set_page_config(page_title='criminal')

st.markdown("# 미 기록자")
st.sidebar.header("Plotting Demo")


notWrite = st.button("범인 색출")
if notWrite:
    today = datetime.today().strftime('%Y-%m-%d')
    query = """
    SELECT member.id, name, menu_name as menu, dt as date FROM member left join (SELECT * FROM lunch_menu where dt=(SELECT CURRENT_DATE))
    as lunch on member.id = lunch.member_name;
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    show = pd.DataFrame(results)
    show
