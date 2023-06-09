from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(3, input_shape=(1,), name='hidden1'))
model.add(Dense(2, name='hidden2'))
model.add(Dense(1, name='output'))
model.summary()

# 1. 전체동결
# model.trainable = False

# 2. 전체동결
# for layer in model.layers:
#     layer.trainable = False

# 3. 부분동결
print(model.layers[0])
# model.layers[0].trainable = False
model.layers[1].trainable = False
# model.layers[2].trainable = False

import pandas as pd
pd.set_option('max_colwidth', -1)
layers = [(layer, layer.name, layer.trainable) for layer in model.layers]
# print(layers)
results = pd.DataFrame(layers, columns=['Layer Type', 'Layer Name', 'Layer Trainable'])
print(results)
