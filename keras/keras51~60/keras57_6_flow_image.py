from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score
from tensorflow.keras.utils import to_categorical

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
print(y_train)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    # vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5,
    zoom_range=0.1,
    shear_range=0.7,
    fill_mode='nearest'
)

augment_size = 40000

np.random.seed(0)
randidx = np.random.randint(x_train.shape[0], size=augment_size)

x_augmented = x_train[randidx].copy()
y_augmented = y_train[randidx].copy()

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

x_augmented = x_augmented.reshape(x_augmented.shape[0], x_augmented.shape[1], x_augmented.shape[2], 1)

x_augmented = train_datagen.flow(x_augmented, y_augmented, batch_size=augment_size, shuffle=False).next()[0]

x_train = np.concatenate([x_train/255., x_augmented], axis=0)
y_train = np.concatenate([y_train, y_augmented], axis=0)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 2. 모델
model = Sequential()
model.add(Conv2D(64, 2, input_shape=(28, 28, 1)))
model.add(Conv2D(64, 2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(10, activation='softmax'))

# 3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics='acc')
es = EarlyStopping(monitor='acc', mode='auto', patience=20, restore_best_weights=True)
model.fit(x_train, y_train, epochs=1, batch_size=128, validation_split=0.2, callbacks=[es])

# 4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

y_predict = np.argmax(model.predict(x_test), axis=1)
print('acc : ', accuracy_score(y_predict, np.argmax(y_test, axis=1)))

import matplotlib.pyplot as plt
plt.figure(figsize=(7, 7))
for i in range(10):
    plt.subplot(2, 10, i+1)
    plt.axis('off')
    plt.imshow(x_train[i+60000], cmap='gray')
    plt.subplot(2, 10, i+11)
    plt.axis('off')
    plt.imshow(x_augmented[i], cmap='gray')
plt.show()
