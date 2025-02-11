import pandas as pd
import streamlit as st
from lunch_menu.db import select_table
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import matplotlib as mpl
from matplotlib import font_manager

st.set_page_config(page_title='STATUS')

st.markdown("# 데이터 분석")
st.sidebar.header("Plotting Demo")

#font_path = os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic-Regular.ttf")
#font_path = "fonts/NanumGothic-Regular.ttf"
#font_prop = font_manager.FontProperties(fname=font_path)
#mpl.rcParams['font.family'] = font_prop.get_name()
#mpl.rcParams['axes.unicode_minus'] = False

data = select_table()

# tab1 데이터
data_tab1 = data
data_tab1 = data_tab1['menu'].value_counts().reset_index()
data_tab1.columns = ['menu', 'count']

# tab2 데이터
data_tab2 = data

# tab3 데이터
data_tab3 = data

tab1, tab2, tab3 = st.tabs(["메뉴 인기 순위", "요인별 선호 음식", "메뉴별 트렌드"])

with tab1:
    rank2, rank1, rank3 = st.columns(3)
    st.balloons()

    with rank2:
        st.write("")
        st.markdown("<p style='text-align: center; font-size: 45px;'>2위</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        silver = data_tab1.iloc[1, 0]
        st.markdown(f"<p style='text-align: center; font-size: 50px; font-weight: bold'>{silver}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 20px;'>{data_tab1.iloc[1,1]}회</p>", unsafe_allow_html=True)
        
    with rank1:
        st.write("")
        st.markdown("<p style='text-align: center; font-size: 45px;'>1위</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        gold = data_tab1.iloc[0, 0]
        st.markdown(f"<p style='text-align: center; font-size: 50px; font-weight: bold'>{gold}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 20px;'>{data_tab1.iloc[0,1]}회</p>", unsafe_allow_html=True)

    with rank3:
        st.write("")
        st.markdown("<p style='text-align: center; font-size: 45px;'>3위</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        bronze = data_tab1.iloc[2, 0]
        st.markdown(f"<p style='text-align: center; font-size: 50px; font-weight: bold'>{bronze}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 20px;'>{data_tab1.iloc[2,1]}회</p>", unsafe_allow_html=True)

with tab2:
    sub_tab1, sub_tab2 = st.tabs(["인원별", "요일별"])

    with sub_tab1:
        who= st.selectbox("인원선택", ["TOM", "cho", "hyun", "JERRY", "SEO", "jiwon", "jacob", "heejin", "lucas", "nuni"])

        if who:
            data_tab2_1 = data_tab2[data_tab2["ename"] == who]
            data_tab2_1 = data_tab2_1["menu"].value_counts().reset_index()
            data_tab2_1.columns = ["menu", "counts"]
            st.write(f"{who}님의 메뉴분포")
            try:
                fig, ax = plt.subplots()
                data_tab2_1.plot(x="menu", y="counts", kind="bar", ax=ax)
                st.pyplot(fig)
                st.write(data_tab2_1["menu"])
            except Exception as e:
                st.write("not enough data")
                print(f"Exception{e}")

    with sub_tab2:
        day= st.selectbox("요일선택", ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"])

        if day:
            data_tab2['day'] = pd.to_datetime(data_tab2['dt'])
            data_tab2['day'] = data_tab2['day'].dt.strftime('%a').str.upper()
            data_tab2_2 = data_tab2
            data_tab2_2 = data_tab2_2[data_tab2_2["day"] == day]
            data_tab2_2 = data_tab2_2["menu"].value_counts().reset_index()
            data_tab2_2.columns = ["menu", "counts"]
            st.write(f"{day} : 메뉴분포")
            try:
                fig, ax = plt.subplots()
                data_tab2_2.plot(x="menu", y="counts", kind="bar", ax=ax)
                st.pyplot(fig)
                st.write(data_tab2_2["menu"])
            except Exception as e:
                st.write("not enough data")
                print(f"Exception{e}")

with tab3:
    data_tab3 = data_tab3[["menu", "dt"]]

    st.line_chart(data_tab3)
