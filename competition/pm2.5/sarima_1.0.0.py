import os
from typing import Any
import numpy as np
import pandas as pd
import time
from xgboost import XGBRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input,Conv1D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
import tensorflow as tf
import glob

# 0. gpu 사용여부
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    except RuntimeError as e:
        print(e)        

# 1.0 train, test, answer 데이터 경로 지정 및 가져오기
path = './_data/finedust/'

train_pm_path = glob.glob(path + 'TRAIN/*.csv')
test_pm_path = glob.glob(path + 'TEST_INPUT/*.csv')
train_aws_path = glob.glob(path + 'TRAIN_AWS/*.csv')
test_aws_path = glob.glob(path + 'TEST_AWS/*.csv')
submission = pd.read_csv('./_data/finedust/answer_sample.csv', index_col=0)

from preprocess_ import bring
train_pm = bring(train_pm_path)
test_pm = bring(test_pm_path)
train_aws = bring(train_aws_path)
test_aws = bring(test_aws_path)



# 1.1 지역 라벨인코딩
label = LabelEncoder()

train_pm['측정소'] = label.fit_transform(train_pm['측정소'])
test_pm['측정소'] = label.transform(test_pm['측정소'])
train_aws['지점'] = label.fit_transform(train_aws['지점'])
test_aws['지점'] = label.transform(test_aws['지점'].ffill())



# 1.2 month, hour 열 생성 & 일시 열 제거
train_pm['month'] = train_pm['일시'].str[:2].astype('int8')
train_pm['hour'] = train_pm['일시'].str[6:8].astype('int8')
train_pm = train_pm.drop(['연도', '일시'], axis=1)

test_pm['month'] = test_pm['일시'].str[:2].astype('int8')
test_pm['hour'] = test_pm['일시'].str[6:8].astype('int8')
test_pm = test_pm.drop(['연도', '일시'], axis=1)

train_aws = train_aws.drop(['연도', '일시'], axis=1)

test_aws = test_aws.drop(['연도', '일시'], axis=1)



# 1.3 train_pm/aws, test_aws의 결측치 제거 ( 일단 imputer )
imputer = IterativeImputer(XGBRegressor())

train_pm['PM2.5'] = imputer.fit_transform(train_pm['PM2.5'].values.reshape(-1 , 1)).reshape(-1,)

train_aws['기온(°C)'] = imputer.fit_transform(train_aws['기온(°C)'].values.reshape(-1 , 1)).reshape(-1,)
test_aws['기온(°C)'] = imputer.transform(test_aws['기온(°C)'].values.reshape(-1 , 1)).reshape(-1,)

train_aws['풍향(deg)'] = imputer.fit_transform(train_aws['풍향(deg)'].values.reshape(-1 , 1)).reshape(-1,)
test_aws['풍향(deg)'] = imputer.transform(test_aws['풍향(deg)'].values.reshape(-1 , 1)).reshape(-1,)

train_aws['풍속(m/s)'] = imputer.fit_transform(train_aws['풍속(m/s)'].values.reshape(-1 , 1)).reshape(-1,)
test_aws['풍속(m/s)'] = imputer.transform(test_aws['풍속(m/s)'].values.reshape(-1 , 1)).reshape(-1,)

train_aws['강수량(mm)'] = imputer.fit_transform(train_aws['강수량(mm)'].values.reshape(-1 , 1)).reshape(-1,)
test_aws['강수량(mm)'] = imputer.transform(test_aws['강수량(mm)'].values.reshape(-1 , 1)).reshape(-1,)

train_aws['습도(%)'] = imputer.fit_transform(train_aws['습도(%)'].values.reshape(-1 , 1)).reshape(-1,)
test_aws['습도(%)'] = imputer.transform(test_aws['습도(%)'].values.reshape(-1 , 1)).reshape(-1,)




















# 2.0 awsmap, pmmap 경로 지정 및 가져오기
from preprocess_ import load_aws_and_pm
awsmap, pmmap = load_aws_and_pm()



# 2.1 awsmap, pmmap의 지역 라벨인코딩
awsmap['Location'] = label.fit_transform(awsmap['Location'])
pmmap['Location'] = label.fit_transform(pmmap['Location'])



# 2.2 awsmap, pmmap을 지역 번호순으로 재정렬 ( 가나다 순서로 번호 인코딩 )
awsmap = awsmap.sort_values(by='Location')
pmmap = pmmap.sort_values(by='Location')



# 2.3 pm관측소로부터 aws관측소의 거리 구하기 ( 17개 x 30개 )
from preprocess_ import distance
dist = distance(awsmap, pmmap)



# 2.4 pm관측소에서 가장 가까운 n(default=3)개의 aws관측소의 인덱스 번호와 환산 가중치 반환
from preprocess_ import scaled_score
result, min_i = scaled_score(dist, pmmap)
dist = dist.values
result = result.values



# 2.5 pm관측소의 날씨 구하기
train_pm = train_pm.values.reshape(17, -1, train_pm.shape[1])
train_aws = train_aws.values.reshape(30, -1, train_aws.shape[1])
test_pm = test_pm.values.reshape(17, -1, test_pm.shape[1])
test_aws = test_aws.values.reshape(30, -1, test_aws.shape[1])

train_pm_aws = []
for i in range(17):
    train_pm_aws.append(train_aws[min_i[i, 0], :, 1:]*result[0, 0] + train_aws[min_i[i, 1], :, 1:]*result[0, 1] + train_aws[min_i[i, 2], :, 1:]*result[0, 2])

train_data = np.concatenate([train_pm, train_pm_aws], axis=2)

test_pm_aws = []
for i in range(17):
    test_pm_aws.append(test_aws[min_i[i, 0], :, 1:]*result[0, 0] + test_aws[min_i[i, 1], :, 1:]*result[0, 1] + test_aws[min_i[i, 2], :, 1:]*result[0, 2])



# pm 의 열
# 측정소 PM2.5 month hour = ( None, 4 )

# aws 의 열
# (지역) 기온 풍향 풍속 강수량 습도       에서 괄호친 열은 제거

# train_pm_aws의 열
# 기온 풍향 풍속 강수량 습도 = ( None, 5 )

# train_data 의 열 ( 훈련 시킬 x값 )
# pm열 + train_pm_aws의 열
# 측정소 PM2.5 month hour + 기온 풍향 풍속 강수량 습도 = ( None, 9 )


















# 3.1 split_x
timesteps = 10

from preprocess_ import split_x
x = split_x(train_data, timesteps).reshape(-1, timesteps, train_data.shape[2])



# 3.2 split_y
y = []
for i in range(train_data.shape[0]):
    y.append(train_data[i, timesteps:, 1].reshape(-1,))
y = np.array(y).reshape(-1,)



# 3.3 train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=323, shuffle=True)



# 3.4 Scaler
scaler = MinMaxScaler()

x_train = x_train.reshape(-1, x.shape[2])
x_test = x_test.reshape(-1, x.shape[2])

x_train[:, 2:], x_test[:, 2:] = scaler.fit_transform(x_train[:, 2:]), scaler.transform(x_test[:, 2:])
# 2: 를 하는 이유는 0번째는 지역, 1번째는 PM2.5
# 지역은 스케일 의미가 없을거같고, PM2.5는 predict해서 나온값을 계속 scale하기 번거로우니까


# 3.5.0 데이터 용량 줄이기 ( float 64 -> float 32 )
x_train=x_train.reshape(-1, timesteps, x.shape[2]).astype(np.float32)
x_test=x_test.reshape(-1, timesteps, x.shape[2]).astype(np.float32)
y_train=y_train.astype(np.float32)
y_test=y_test.astype(np.float32)


from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import itertools

p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
tmp_model = None
best_mdl = None

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            tmp_mdl = SARIMAX(y_train, exog=None, order=param, seasonal_order=param_seasonal, enforce_stationarity=True, enforce_invertibility=True)
            res = tmp_mdl.fit()
            print('sarimax{}x{}12 - aic:{}'.format(param, param_seasonal, res.aic))
            if res.aic < best_aic:
                best_aic = res.aic
                best_pdq = param
                best_seasonal_pdq = param_seasonal
                best_mdl = tmp_mdl
        except:
            continue

print('best sarimax{}x{}12 model - aic:{}'.format(best_pdq, best_seasonal_pdq, best_aic))

