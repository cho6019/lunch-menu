import streamlit as st
import requests
import datetime


st.set_page_config(page_title="API", page_icon="🍽️")

st.markdown("# 🍽️ API")
st.sidebar.header("나이계산기")

dt = st.date_input('생일입력', min_value=datetime.date(1900,1,1))
if st.button("나이계산"):
    headers={
        'accept': 'application/json'
    }
    response = requests.get(f'https://agecalculator.cho6019.store/api/py/ageCalculator/birthday/{dt}', headers=headers)
    st.write(response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        age = result["age"]
        st.write(f'당신의 나이는 {age}세!')
        st.success(f'나이계산{dt}')
    else:
        st.write(f'what?{response.status_code}')
    
    