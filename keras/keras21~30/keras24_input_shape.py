from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
# 1. 데이터
datasets = load_boston()
x = datasets.data
y = datasets['target']

print(type(x))     # <class 'numpy.ndarray'>
print(x)


# (사이킷런 1.2부터 임포트 안됨)
# pip uninstall scikit-learn
# pip install scikit-learn==1.1

print(np.min(x), np.max(x))     # 0.0 711.0


x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=333)
# scaler = MinMaxScaler()

# scaler = StandardScaler()

# scaler = MaxAbsScaler()

scaler = RobustScaler()

scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

print(np.min(x_test), np.max(x_test))     # 0.0 1.0


# 2. 모델
model = Sequential()
# model.add(Dense(1, input_dim=13))
model.add(Dense(1, input_shape=(13,)))


# 데이터가 3차원이면 (시계열 데이터)
# (1000, 100, 1) -> input_shape(100, 1)
# 데이터가 4차원이면 (이미지 데이터)
# (60000, 32, 32, 3) -> input_shape(32, 32, 3)



# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=10)

# 4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

# 
# (MinMaxScaler) 
# (StandardScaler) 
# (MaxAbsSclaer) 
# (RobustScaler)