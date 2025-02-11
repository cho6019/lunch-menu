import streamlit as st
from lunch_menu.db import get_connection
from lunch_menu.db import insert_menu
from lunch_menu.db import select_table
from lunch_menu.keyword import normalize_menu

st.set_page_config(page_title='INPUT')

st.markdown("# 신규 정보입력")
st.sidebar.header("Plotting Demo")

# 멤버 인덱스 추출
members = {"TOM": 1, "cho": 2, "hyun": 3, "JERRY": 4, "SEO": 5, "jiwon": 6, "jacob": 7, "heejin": 8, "lucas": 9, "nuni": 10}
new_list = list(members.keys())


# 입력 정보 생성 코드
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.selectbox(
        "먹은 사람", new_list)

dt = st.date_input("먹은 날짜")

# 정보 삽입 버튼
isPress = st.button("메뉴 저장")
if isPress:
    if menu_name and member_name and dt:
        menu_name = normalize_menu(menu_name)
        if insert_menu(menu_name, (new_list.index(member_name)+1), dt):
            st.success(f"{menu_name},{member_name},{dt}가 입력되었습니다")
        else:
            st.warning(f"금일 이미 입력")
    else:
        st.warning(f"모든 값을 입력해주세요!")



