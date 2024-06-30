# from bikes_data import data_preprocessing

def bikes_da():
    import pandas as pd
    import streamlit as st
    import seaborn as sns
    import folium
    import matplotlib.pyplot as plt
    import streamlit.components.v1 as components
    
    plt.rc('font',family='Malgun Gothic') 

    @st.cache_data
    def data_preprocessing():
        bikes=pd.DataFrame()
        # for i in range(3):
        # bikes_temp = pd.read_csv(f"data\서울특별시 공공자전거 대여정보_201906_{i+1}.csv", encoding='cp949')
        bikes_temp1 = pd.read_csv("https://drive.google.com/uc?id=1uhG-vQibMO4MYe8I8krs-tV_632eqrWZ", encoding='cp949')
        bikes=pd.concat([bikes,bikes_temp1])  #,bikes_temp2,bikes_temp3
            
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
        hourly_dayofweek_ride = bikes.pivot_table(index='대여시간대',columns='요일',values='자전거번호',aggfunc=['count'])
        fig, ax = plt.subplots(figsize=(20,4))
        ax=sns.heatmap(data=hourly_dayofweek_ride,annot=True,fmt='d')
        ax.set_title(f"대여시간대 & 요일별 이용건수")
        st.pyplot(fig)


    with tab3:
        st.write("tab2")
    
        
    with tab4:
        
        @st.cache_data
        def get_data():
            rent_bike = bikes.pivot_table(index=['대여 대여소명','대여점 위도','대여점 경도'],
                                columns=['주말구분'],
                                values='자전거번호',
                                aggfunc='count')
            
            weeekend_house50 = rent_bike.nlargest(50,'주말')['주말'].reset_index()
            days_house50 = rent_bike.nlargest(50,'평일')['평일'].reset_index()
            
            return weeekend_house50, days_house50

        weeekend_house50, days_house50 = get_data()
        lat = bikes['대여점 위도'].mean()
        lon = bikes['대여점 경도'].mean()
        center = [lat, lon]
        map2 = folium.Map(location = center, zoom_start = 11)
        for i in weeekend_house50.index:
            sub_lat = weeekend_house50.loc[i,'대여점 위도']
            sub_lon = weeekend_house50.loc[i,'대여점 경도']
            name = weeekend_house50.loc[i,'대여 대여소명']
            
            folium.Marker(location = [sub_lat, sub_lon],
                        popup = name).add_to(map2) 
        # 지도 제목과 캡션 추가
        st.subheader("주말 인기 대여소 Top 50")
        st.caption("주말에 인기 있는 대여소 TOP50을 표시한 것으로 주로 한강변, 호수나 공원 근처이다.")
 
         #지도 시각화
        components.html(map2._repr_html_(), height=400)
        st.markdown(""" 
                * 가족 동반 나들이로 이용하는 경우에 대비하여 아동용 따릉이나 안전용 헬멧 등을 비치하자. 
                * 따릉이를 이용하는 사람들이 많이 모이게 되니 안전 수칙을 알리는 표지판, 물을 마실 수 있는 개수대, 쓰레기통 비치 등에 신경 쓰자.""")
        
        for i, row in days_house50.iterrows():
            sub_lat = row['대여점 위도']
            sub_lon = row['대여점 경도']
            name = row['대여 대여소명']
            
            folium.Marker(location = [sub_lat, sub_lon],
                  popup = name,
                  icon=folium.Icon(color='red',icon='bicycle',prefix='fa')).add_to(map2) 
            
        st.subheader("평일 인기 대여소 Top 50")
        st.caption("평일에 인기 있는 대여소 TOP50을 표시한 것으로 많은 대여소가 주말에 인기 있는 대여소와 일치한다.")
 
        #지도 시각화
        components.html(map2._repr_html_(), height=400)
        
        st.markdown("""
                    * 예외적인 곳은 한강변 자전거 도로를 이용해서 출퇴근하는 사람들이 강변 안쪽 회사 밀집 지역을 이용하는 경우이다.
                    * 한강변에서 회사 밀집 지역으로 진입하는 도로에 자전거 도로를 편하게 만들어서 좀더 많은 사람들이 자전거로 출퇴근할 수 있도록 유도하자.""")

