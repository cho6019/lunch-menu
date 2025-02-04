import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv


load_dotenv()
DB_CONFIG = {
   "user": os.getenv("DB_USERNAME"),
   "dbname": os.getenv("DB_NAME"),
   "password": os.getenv("DB_PASSWORD"),
   "host": os.getenv("DB_HOST"),
   "port": os.getenv("DB_PORT")
}
#환경변수를 통한 설정(보안)

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_name, dt):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
           "INSERT INTO lunch_menu(menu_name, member_name, dt) VALUES (%s, %s, %s);",
            (menu_name, member_name, dt)
        )
        conn.commit()
        cursor.close()
        conn.close()

st.title("순신점심기록장")

st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.text_input("먹은 사람", value="TOM")
dt = st.date_input("얌얌 날짜")

isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_name and dt:
        insert_menu(menu_name, member_name, dt)
        st.success(f"버튼{isPress}:{menu_name},{member_name},{dt}")
    else:
        st.warning(f"모든 값을 입력해주세요!")


st.subheader("확인")
query = """SELECT 
menu_name AS menu, 
member_name AS ename, 
dt 
FROM lunch_menu 
ORDER BY dt DESC"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
#conn.commit()
cursor.close()

#selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
select_df = pd.DataFrame(rows, columns=['menu','ename','dt'])
select_df

st.subheader("통계")
df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]

#gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
gdf = select_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x="ename", y="menu", kind="bar")

gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)

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
        (not_na_df.iloc[i, 2], not_na_df.iloc[i, 0], not_na_df.iloc[i, 1]))
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
