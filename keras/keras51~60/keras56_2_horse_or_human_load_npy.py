# 불러와서 모델 완성
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from sklearn.model_selection import train_test_split
# 1. 데이터
save_path = 'd:/study_data/_save/horse-or-human/'

# horse_human_x_train = np.load(save_path + 'keras56_horse_human_x_train.npy')
# horse_human_x_test = np.load(save_path + 'keras56_horse_human_x_test.npy')
# horse_human_y_train = np.load(save_path + 'keras56_horse_human_y_train.npy')
# horse_human_y_test = np.load(save_path + 'keras56_horse_human_y_test.npy')

horse_human_x = np.load(save_path + 'keras56_horse_human_x.npy')
horse_human_y = np.load(save_path + 'keras56_horse_human_y.npy')

horse_human_x_train, horse_human_x_test, horse_human_y_train, horse_human_y_test = train_test_split(horse_human_x, horse_human_y, train_size=0.7, shuffle=True, random_state=123)

# 2. 모델구성
model = Sequential()
model.add(Conv2D(32, (2, 2), input_shape=(250, 250, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# 3. 컴파일, 훈련
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
hist = model.fit(horse_human_x_train, horse_human_y_train, epochs=30, validation_data=(horse_human_x_test, horse_human_y_test))

loss = hist.history['loss']
val_loss = hist.history['val_loss']
acc = hist.history['acc']
val_acc = hist.history['val_acc']

import matplotlib.pyplot as plt
plt.figure(figsize=(9,6))
plt.subplot(1, 2, 1)
plt.plot(loss, label='loss')
plt.plot(val_loss, label='val_loss')
plt.grid()
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(acc, label='acc')
plt.plot(val_acc, label='val_acc')
plt.grid()
plt.legend()
plt.show()

# 4. 평가, 예측
loss = model.evaluate(horse_human_x_test, horse_human_y_test)
print('loss : ', loss)

y_predict = np.round(model.predict(horse_human_x_test))
from sklearn.metrics import accuracy_score
acc = accuracy_score(horse_human_y_test, y_predict)
print('acc : ', acc)