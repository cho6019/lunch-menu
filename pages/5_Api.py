import streamlit as st
import requests


st.set_page_config(page_title="API", page_icon="🍽️")

st.markdown("# 🍽️ API")
st.sidebar.header("나이계산기")

dt = st.date_input('생일입력')
if st.button("나이계산"):
    response = requests.get('https://ac.sunsin.shop/api/py/ageCalculator/{dt}')
    result = response.json()
    st.write(f"당신의 나이는 {result['age']}세!")
    
    st.success(f'나이계산{dt}')
    
    