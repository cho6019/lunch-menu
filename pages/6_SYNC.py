import streamlit as st
import requests
import pandas as pd
import json
from lunch_menu.db import select_table_sync, insert_menu
from pandasql import sqldf



st.set_page_config(page_title="API", page_icon="🍽️")

def api_url():
    ep = "https://raw.githubusercontent.com/cho6019/nextjs-fastapi-starter/refs/heads/0.6/korea/endpoints.json"
    res = requests.get(ep)
    r = res.json()
    list_url = []
    for i in r['endpoints']:
        if i['name'] != 'cho' and i['name'] != 'heejin':
            list_url.append(i['url'])
    return list_url
        



st.markdown("# SYNC")
st.sidebar.header("모두의 점심 데이터 비교 합치기")

do_sync = st.button("데이터 동기화 하기")

members = {"TOM": 1, "cho": 2, "hyun": 3, "JERRY": 4, "SEO": 5, "jiwon": 6, "jacob": 7, "heejin": 8, "lucas": 9, "nuni": 10, "CHO": 2, "HYUN": 3,
           "JIWON": 6, "JACOB": 7, "HEEJIN": 8, "LUCAS": 9, "NUNI": 10}

if do_sync:
    list_url = api_url()
    url_count = 0
    row_count = 0
    for i in list_url:
        r = requests.get(i)
        data = r.json()
        df = pd.DataFrame(data)
        my_df = select_table_sync()
        
        query="""
        SELECT df.menu_name, df.name, df.dt
        FROM df left join my_df on df.dt=my_df.dt AND df.name=my_df.name
        WHERE my_df.dt is null
        """
        pysqldf = lambda q: sqldf(q, globals())
        result = pysqldf(query)
        st.write(result)
        if len(result) >= 1:
            url_count += 1
            row_count += len(result)
            for _, row in result.iterrows():
                insert_menu(row["menu_name"], members[row["name"]], row["dt"])
    st.success(f"작업완료 - 새로운 원천 {url_count}곳에서 총 {row_count}건을 새로 추가 하였습니다.")
        
        
        