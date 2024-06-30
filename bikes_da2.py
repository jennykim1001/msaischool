# from bikes_data import data_preprocessing

def bikes_da():
    import pandas as pd
    import streamlit as st
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.rc('font',family='Malgun Gothic')

    @st.cache_data
    def data_preprocessing():
        bikes=pd.DataFrame()
        for i in range(3):
            bikes_temp = pd.read_csv(f"data\서울특별시 공공자전거 대여정보_201906_{i+1}.csv", encoding='cp949')
            bikes=pd.concat([bikes,bikes_temp])
            
        #데이터 전처리
        bikes.isnull().sum()
        bikes['대여일시']=bikes['대여일시'].astype('datetime64[ms]')

        #파생변수 생성
        요일 =['월','화','수','목','금','토','일']
        bikes['요일']=bikes['대여일시'].dt.dayofweek.apply(lambda x : 요일[x])
        bikes['일자']=bikes['대여일시'].dt.day
        bikes['주말구분']=bikes['대여일시'].dt.dayofweek.apply(lambda x : "평일" if x<5 else "주말" )
        bikes['대여시간대']=bikes['대여일시'].dt.hour

        # 위도, 경도 가져오기
        bike_shop = pd.read_csv("data\공공자전거 대여소 정보_23_06.csv", encoding='cp949')
        bike_gu=bike_shop[['자치구','대여소번호', '보관소(대여소)명','위도', '경도']]
        bike_gu = bike_gu.rename(columns={'보관소(대여소)명':'대여소명'})
        bikes = pd.merge(bikes,bike_gu,left_on='대여 대여소번호',right_on='대여소번호')
        bikes = bikes.drop(['대여소번호','대여소명'],axis=1)
        bikes = bikes.rename(columns={'자치구':'대여구','위도':'대여점 위도','경도':'대여점 경도'})
        
        return bikes

    bikes = data_preprocessing()
    tab1, tab2, tab3, tab4 = st.tabs(["데이터 확인", "시간적 분석", "시간&공간 분석", "인기대여소"])

    with tab1:
        # st.write("tab1")
        st.dataframe(bikes.head(20))

    with tab2:
        # 요일/일자/대여시간대별 이용건수 분석
        chart_da_name=['요일','일자','대여시간대']
        for i in chart_da_name:
            fig,ax = plt.subplots(figsize=(15,4))
            ax= sns.countplot(data=bikes, x=i)
            ax.set_title(f"{i}별 이용건수")
            st.pyplot(fig)
            
        st.markdown('''
            **1. 요일별 분석**
            * 평일보다는 주말에 따릉이 이용건수가 많고 주말 중에서는 토요일에 가장 이용건수가 많다.
            * 주말에 인기 있는 대여소 근처에 대여소를 추가로 설치하거나 따릉이를 추가 배치할 필요가 있다.
            
            **2. 일자별 분석**
            * 6일이 현충일이지만 비가 와서 이용건수가 적다. 강수량에 영향을 많이 받는다.
            * 일회용 우비 등을 비치해서 비 오는 날도 따릉이 이용에 불편이 없도록 한다.
            
            **3. 시간대별 분석** 
            * 출퇴근 시간대를 중심으로 이용건수가 많고 오전<오후<저녁 순으로 이용건수가 증가한다.
            * 출퇴근 시간대에 많이 이용되는 대여소에 따릉이를 추가 배치하자.
            ''')
            
            # # # 일자별로 이용수 분석
            # fig, ax = plt.subplots(figsize=(15,4))
            # ax = sns.countplot(data=bikes,x='일자')
            # ax.set_title("일자별 이용건수")

        # # # 대여시간대별로 이용수 분석
        # fig, ax = plt.subplots(figsize=(15,4))
        # ax= sns.countplot(data=bikes,x='대여시간대',hue="주말구분")
        # st.pyplot(fig)

        # 대여시간대별, 요일별 이용건수 분석 - 히트맵
        # bikes['대여시간대']=bikes['대여일시'].dt.hour
        hourly_dayofweek_ride = bikes.pivot_table(index='대여시간대',columns='요일',values='자전거번호',aggfunc=['count'])
        fig, ax = plt.subplots(figsize=(20,4))
        ax=sns.heatmap(data=hourly_dayofweek_ride,annot=True,fmt='d')
        ax.set_title(f"대여시간대 & 요일별 이용건수")
        st.pyplot(fig)


    with tab3:
        # # 대여구 별 이용건수 분석
        # 구별이용시간평균 = bikes.pivot_table( index='대여구',values='',aggfunc='mean') \
        #                         .sort_values(by='이용시간', ascending=True)  \
        #                         .reset_index()
        # 구별이용시간평균.plot(kind='barh', title='구별 이용시간 평균',figsize=(12,6),color='r')
        # plt.show()

        # # 대여구 별 이용시간 분석
        # 구별이용시간평균 = bikes.pivot_table( index='대여구',values='이용시간',aggfunc='mean') \
        #                         .sort_values(by='이용시간', ascending=True)  \
        #                         .reset_index()
        # 구별이용시간평균.plot(kind='barh', title='구별 이용시간 평균',figsize=(12,6),color='r')
        # plt.show()
        st.write("tab2")
        

        
    with tab4:
        st.write("tab4")
