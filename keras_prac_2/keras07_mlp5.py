import numpy as np  
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. 데이터
x = np.array([range(10), range(21,31), range(201, 211)])    # (3, 10)
x = x.T   # (10, 3)

y = np.array([[1,2,3,4,5,6,7,8,9,10],
              [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]) # (2, 10)

y = y.T     #(10, 2)

# 2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=3))
model.add(Dense(100))
model.add(Dense(1000))
model.add(Dense(100))
model.add(Dense(10))
model.add(Dense(2))

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x, y, epochs=1000, batch_size=1)

# 4. 평가, 예측
loss = model.evaluate(x, y)
print("loss: ", loss)

result = model.predict([[9, 30, 210]])
print("[[9, 30, 210]]의 예측값 : ", result)