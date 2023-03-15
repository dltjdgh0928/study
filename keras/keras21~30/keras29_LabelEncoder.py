# 데이콘 따릉이 문제풀이
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd

# 1. 데이터
path = './_data/wine/' # . 은 현재 폴더(STUDY)를 의미함

# train_csv = pd.read_csv('./_data/ddarung/train.csv')
train_csv = pd.read_csv(path + 'train.csv', index_col=0)

print(train_csv)
print(train_csv.shape)      # (5497, 10)


test_csv = pd.read_csv(path + 'test.csv', index_col=0)

print(test_csv)
print(test_csv.shape)      # (1000, 12)

from sklearn.preprocessing import LabelEncoder, RobustScaler
le = LabelEncoder()
le.fit(train_csv['type'])
aaa = le.transform(train_csv['type'])
print(aaa)
print(type(aaa))        # <class 'numpy.ndarray'>
print(aaa.shape)
# print(np.unique(aaa, return_counts=True))

train_csv['type'] = aaa
print(train_csv)
test_csv['type'] = le.transform(test_csv['type'])

print(le.transform(['red', 'white']))
print(le.transform(['white', 'red']))

'''
# ================================================================================================= #

print(train_csv.columns)

# Index(['hour', 'hour_bef_temperature', 'hour_bef_precipitation',
#       'hour_bef_windspeed', 'hour_bef_humidity', 'hour_bef_visibility',
#       'hour_bef_ozone', 'hour_bef_pm10', 'hour_bef_pm2.5', 'count'],
#       dtype='object')

print(train_csv.info())

#  0   hour                    1459 non-null   int64
#  1   hour_bef_temperature    1457 non-null   float64
#  2   hour_bef_precipitation  1457 non-null   float64
#  3   hour_bef_windspeed      1450 non-null   float64
#  4   hour_bef_humidity       1457 non-null   float64
#  5   hour_bef_visibility     1457 non-null   float64
#  6   hour_bef_ozone          1383 non-null   float64
#  7   hour_bef_pm10           1369 non-null   float64
#  8   hour_bef_pm2.5          1342 non-null   float64
#  9   count                   1459 non-null   float64


print(train_csv.describe())

print(type(train_csv))      # <class 'pandas.core.frame.DataFrame'>

######################### 결측치 처리 #############################
# 결측치 처리 1. 제거
print(train_csv.isnull().sum())
train_csv = train_csv.dropna()      ### 결측지 제거 ###
print(train_csv.isnull().sum())
print(train_csv.info())
print(train_csv.shape)      #(1328, 10)
print(type(train_csv))      # <class 'pandas.core.frame.DataFrame'>

######################### train_csv데이터에서 x와 y를 분리 ##############################
x = train_csv.drop(['count'], axis=1)
print(x)

y = train_csv['count']
print(y)
######################### train_csv데이터에서 x와 y를 분리 ##############################


x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, train_size=0.7, random_state=1)

# print(x_train.shape, x_test.shape)      #(1021, 9), (438, 9) -> (929, 9), (399, 9)
# print(y_train.shape, y_test.shape)      #(1021,), (438,) -> (929,), (399,)

# 2. 모델구성
model = Sequential()
model.add(Dense(32, input_dim=9))
model.add(Dense(64))
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(8))
model.add(Dense(1))

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=0)

# 4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print("loss : ", loss)
    

'''