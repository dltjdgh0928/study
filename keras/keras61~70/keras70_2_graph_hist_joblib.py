from tensorflow.keras.datasets import mnist
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, GlobalAveragePooling2D
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
from tensorflow.python.keras.callbacks import EarlyStopping, History
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import time
import joblib

tf.random.set_seed(337)

# 1. 데이터
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 2. 모델구성
hist = joblib.load(open('./_save/keras70_joblib_save.joblib', "rb"))
model = load_model('./_save/keras70_1_mnist_graph.h5')

# hist_df = pd.DataFrame(hist.history)
# model.save('./_save/keras70_1_mnist_graph.h5')
# joblib.dump(hist_df, './_save/keras70_joblib_save.joblib')



# 4. 평가, 예측
result = model.evaluate(x_test, y_test)
print('result : ', result)
print('loss :', result[0])
print('acc', result[1])
y_predict = model.predict(x_test)
acc = accuracy_score(np.argmax(y_test,axis=1), np.argmax(y_predict,axis=1))
print(f'acc : {acc}')




import matplotlib.pyplot as plt 
plt.figure(figsize=(9, 5))

# 1
plt.subplot(2, 1, 1)
plt.plot(hist['loss'], marker='.', c='red', label='loss')
plt.plot(hist['val_loss'], marker='.', c='blue', label='val_loss')
plt.grid()
plt.title('loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend(loc='upper right')

# 2
plt.subplot(2, 1, 2)
plt.plot(hist['acc'], marker='.', c='red', label='acc')
plt.plot(hist['val_acc'], marker='.', c='blue', label='val_acc')
plt.grid()
plt.title('acc')
plt.xlabel('epochs')
plt.ylabel('acc')
plt.legend(['acc', 'val_acc'])

plt.show()

# plt.plot(hist.history['val_acc'], label='val_acc')
# plt.show()

