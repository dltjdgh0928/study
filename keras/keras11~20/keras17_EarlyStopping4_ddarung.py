import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.metrics import r2_score
from tensorflow.python.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# 1. 데이터
# 1.1 경로, 가져오기
path = './_data/ddarung/'
path_save = './_save/ddarung/'

train_csv = pd.read_csv(path + 'train.csv', index_col=0)
test_csv = pd.read_csv(path + 'test.csv', index_col=0)

# 1.2 확인사항 5가지
print(train_csv.shape, test_csv.shape)
print(train_csv.columns, test_csv.columns)
print(train_csv.info(), test_csv.info())
print(train_csv.describe(), test_csv.describe())
print(type(train_csv), type(test_csv))

# 1.3 결측지 제거
print(train_csv.isnull().sum())
train_csv = train_csv.dropna()
print(train_csv.isnull().sum())

# 1.4 x, y 분리
x = train_csv.drop(['count'], axis=1)
y = train_csv['count']

# 1.5 train, test 분리
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=12345, shuffle=True)

# 2. 모델구성
model = Sequential()
model.add(Dense(32, input_dim=9, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=200, restore_best_weights=True)
hist = model.fit(x_train, y_train, epochs=300, batch_size=5, validation_split=0.2, verbose=1, callbacks=[es])

# 4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

y_predict = model.predict(x_test)
r2 = r2_score(y_test, y_predict)
print('r2 : ', r2)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.figure(figsize=(9,6))
plt.plot(hist.history['loss'], marker='.', c='red', label='로스')
plt.plot(hist.history['val_loss'], marker='.', c='blue', label='발_로스')
plt.title('따릉이')
plt.legend()
plt.grid()
plt.xlabel('epochs')
plt.ylabel('loss, val_loss')
plt.show()

# 4.1 내보내기
submission = pd.read_csv(path + 'submission.csv', index_col=0)
y_submit = model.predict(test_csv)
submission['count'] = y_submit

submission.to_csv(path_save + 'submit_ES_0310_0737.csv')