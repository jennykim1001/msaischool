import streamlit as st
import bikes_da2

st.set_page_config(page_title="따릉이")

# 사이드바 화면
st.sidebar.header("로그인")
user_id = st.sidebar.text_input('아이디(ID) 입력', value="streamlit", max_chars=15)
user_password = st.sidebar.text_input('패스워드(Password) 입력', value="", type="password")

if user_password == '1234':

    st.sidebar.header("== Heeya's Portfolio ==")
    selectbox_options = ["",'유성우', '따릉이'] # 셀렉트 박스의 선택 항목
    menu = st.sidebar.selectbox('메뉴선택', selectbox_options, index=0) # 셀렉트박스의 항목 선택 결과
    # st.sidebar.write(your_option)

    if menu == "유성우":
        st.write("유성우 데이터 분석 >>>>")

    elif menu == "따릉이":
        st.write("따릉이 데이터 분석 >>>>")
        bikes_da2.bikes_da()
    else:
        st.write("환영합니다!!!")

    # # 메인(Main) 화면
    # if your_option=='환율조회':
    #     # pass
    #     exchange.exchange_main()
    # else:
    #     pass
    


# pip list --format=freeze > requirements.txt
    