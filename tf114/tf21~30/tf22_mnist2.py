# pip install keras==1.2.2
# from tensorflow.keras.datasets import mnist
from keras.datasets import mnist
import keras
import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score
from keras.utils.np_utils import to_categorical
# print(keras.__version__)
tv = tf.compat.v1

# tf.compat.v1.disable_eager_execution()
# tf.set_random_seed(337)
# tf.random.set_seed(337)
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#     except RuntimeError as e:
#         print(e)        

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], -1).astype('float32')
x_test = x_test.reshape(x_test.shape[0], -1).astype('float32')

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
output_node = y_train.shape[1]

xp = tv.placeholder('float', shape = [None, x_train.shape[1]])
yp = tv.placeholder('float', shape = [None, output_node])

hidden_node1 = 64

w1 = tv.get_variable('weight1', shape=[x_train.shape[1], hidden_node1])
# w1 = tv.Variable(tv.random.normal([x_train.shape[1], hidden_node1]), name='weight1')

b1 = tv.Variable(tv.zeros(hidden_node1), name='bias1')
layer1 = tv.matmul(xp, w1) + b1
dropout1 = tv.nn.dropout(layer1, rate=0.3)

w2 = tv.Variable(tv.random.normal([hidden_node1, output_node]), name='weight2')
b2 = tv.Variable(tv.zeros([output_node]), name='bias2')
hypothesis = tv.matmul(dropout1, w2) + b2


# loss = tf.reduce_mean(-tf.reduce_sum(yp*tf.nn.log_softmax(hypothesis), axis=1))
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=yp, logits=hypothesis))
train = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)
    
epochs = 10

sess = tv.Session()
sess.run(tv.global_variables_initializer())

for step in range(epochs):
    _, loss_val = sess.run([train, loss], feed_dict={xp:x_train, yp:y_train})
    y_pred = sess.run(hypothesis, feed_dict={xp:x_test})
    print(f'epoch : {step+1}\t\t{(step+1)*100/epochs}% complete\t\tloss : {loss_val}')
print('acc : ', accuracy_score(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1)))    



