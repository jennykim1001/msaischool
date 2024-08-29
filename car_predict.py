import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score,root_mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import csv
import streamlit as st

def indata():
    fields = ['id','model','year','transmission','mileage','fuelType','tax','mpg','engineSize']
    data = {}

    # 데이터 입력
    for i in fields:
        #value = input(f'{i} : ')
        value = st.text_input(f'{i} : ')
        data[i] = value

    filename = 'used_car_x_test1.csv'
    with open(filename,'w',newline='') as f:
        w = csv.DictWriter(f,fieldnames=fields)
        w.writeheader()   #열 제목을 파일에 작성
        w.writerow(data)    #사용자 입력 데이터를 파일에 작성
    
    return filename

def model(filename):
    # 데이터 불러오기 ======================================================
    df_X_train = pd.read_csv('aidata/used_car_x_train.csv')
    # df_X_test = pd.read_csv('data/used_car_x_test.csv')/
    df_X_test = pd.read_csv(filename)
    df_y_train = pd.read_csv('aidata/used_car_y_train.csv')

    #전처리 ================================================================
    #1. 범주형, 숫자형 데이터로 분리
    #범주형 데이터
    df_X_train['model'] = df_X_train['model'].str.replace(" ","")   # 공백 없애기
    X_train_word = df_X_train[['model','transmission','fuelType']]
    X_test_word = df_X_test[['model','transmission','fuelType']]

    #수치 데이터
    X_train_num = df_X_train.drop(['id','model','transmission','fuelType'],axis=1)
    X_test_num = df_X_test.drop(['id','model','transmission','fuelType'],axis=1)

    #2. 데이터 스케일링 - 수치형데이터
    #개체 생성
    scaler = MinMaxScaler()
    X_train_num_scale =scaler.fit_transform(X_train_num) 
    X_test_num_scale = scaler.transform(X_test_num)
    #데이터 프레임 설정
    df_train_num = pd.DataFrame(X_train_num_scale,columns=X_train_num.columns)
    df_test_num = pd.DataFrame(X_test_num_scale,columns=X_test_num.columns)

    #3. 원핫 인코딩 - 범주형 데이터
    df_train_word = pd.get_dummies(X_train_word)
    df_test_word = pd.get_dummies(X_test_word)

    # 원핫인코딩 후에 훈련데이터랑 테스트 데이터 열(칼럼) 체크
    # 훈련 데이터 목록
    train_cols = set(df_train_word.columns)   #집합, {}, 키값없는 딕셔너리, 합집합/교집합/차집합

    # 테스트 데이터 목록
    test_cols = set(df_test_word.columns)
    missing_test = train_cols - test_cols
    missing_train = test_cols - train_cols

    if len(missing_test) >0 :
        for i in missing_test:
            df_test_word[i] =0

    if len(missing_train) >0 :
        for i in missing_train:
            df_train_word[i] =0

    # 4. 수치형데이터, 범주형 데이터 병합
    df_train = pd.concat([df_train_num,df_train_word],axis=1)
    df_test = pd.concat([df_test_num,df_test_word],axis=1)

    # 모델링 ================================================================
    # 머신러닝 - 지도학습
    # 1. 독립변수(X), 종속변수(y)
    X = df_train
    y = df_y_train['price']

    # 2. 데이터 7:3으로 나누기
    X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=0.3,random_state=0)

    # 3. 회귀예측 모델 생성 및 학습, 평가
    # 3-1. 모델 개체 생성
    RForest_model = RandomForestRegressor(random_state=0)

    # 3-2. 학습
    RForest_model.fit(X_train,y_train)

    # 평가 - score(=R2, 테스트독립변수, 테스트종속변수)
    print("R2 score : ", RForest_model.score(X_train,y_train))
    # 평가 - RMSE
    x_predict = RForest_model.predict(X_val)
    print('RandomForestRegressor:', root_mean_squared_error(y_val,x_predict))   #예측값

    # 활용 ================================================================
    # print(X_train.columns)
    df_test = df_test[['year', 'mileage', 'tax', 'mpg', 'engineSize', 'model_A1', 'model_A2',
        'model_A3', 'model_A4', 'model_A5', 'model_A6', 'model_A7',
        'model_A8', 'model_Q2', 'model_Q3', 'model_Q5', 'model_Q7',
        'model_Q8', 'model_R8', 'model_RS3', 'model_RS4', 'model_RS5',
        'model_RS6', 'model_RS7', 'model_S3', 'model_S4', 'model_S5',
        'model_S8', 'model_SQ5', 'model_SQ7', 'model_TT',
        'transmission_Automatic', 'transmission_Manual',
        'transmission_Semi-Auto', 'fuelType_Diesel', 'fuelType_Hybrid',
        'fuelType_Petrol']]

    y_predict = RForest_model.predict(df_test)
    st.write(f'예상 가격은 {y_predict[0]} 입니다')

def aiml_main():
    filename = indata()
    if st.button("예측"):   #st.button("예측")==True
        model(filename)

if __name__=='__main__':
    aiml_main()
        


