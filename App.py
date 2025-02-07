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
st.title("순신점심기록장")

# 필요정보 추출
df = pd.read_csv('note/menu.csv')
start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                     var_name='dt', value_name='menu')
not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
select_df = pd.DataFrame(not_na_df, columns=['menu','ename','dt'])
gdf = select_df.groupby('ename')['menu'].count().reset_index()
name_list = gdf['ename']

# 안 쓴 사람 찾기
notWrite = st.button("범인 색출")
if notWrite:
    today = datetime.today().strftime('%Y-%m-%d')
    query = """
    SELECT name FROM member left join (SELECT * FROM lunch_menu where dt=(SELECT CURRENT_DATE))
    as lunch on member.id = lunch.member_name
    WHERE lunch.menu_name is null;
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    for result in results:
        st.write(result)


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


# TODO
# CSV 로드해서 한번에 다 디비에 INSERT 하는거
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
"""

if importPress:
    df = pd.read_csv('note/menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                        var_name='dt', value_name='menu')

    not_na_df = melted_df[~melted_df['menu'].isin(['-', 'x', '<결석>'])]

    for _, row in not_na_df.iterrows():
        insert_menu(row['menu'], row['ename'], row['dt'])

    st.success(f"벌크인서트 성공")
"""
