import streamlit as st
from lunch_menu.db import get_connection
import pandas as pd
from lunch_menu.keyword import normalize_menu

st.set_page_config(page_title='BULK')

st.markdown("# 데이터 불러오기 / 삭제")
st.sidebar.header("Plotting Demo")

st.subheader("벌크 인서트")
importPress = st.button("한방에 인서트")

if importPress:
    df = pd.read_csv('note/menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                     var_name='dt', value_name='menu')
    not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
    not_na_df['menu'] = not_na_df['menu'].apply(normalize_menu)

    members = {"TOM": 1, "cho": 2, "hyun": 3, "JERRY": 4, "SEO": 5, "jiwon": 6, "jacob": 7, "heejin": 8, "lucas": 9, "nuni": 10}
    new_list = list(members.keys())

    conn = get_connection()
    with conn.cursor() as cur:
        for i in range(not_na_df.shape[0]):
            cur.execute("INSERT INTO lunch_menu(menu_name, member_name, dt) VALUES (%s, %s, %s);",
            (not_na_df.iloc[i, 2], new_list.index(not_na_df.iloc[i, 0])+1, not_na_df.iloc[i, 1]))
    conn.commit()
    st.write('DONE!')


st.divider()

st.subheader("데이터 전체 삭제")
delPress = st.button("돌이킬 수 없습니다")

if delPress:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE lunch_menu;")
    conn.commit()
    st.write("Done")
