# pip install keras==1.2.2
# from tensorflow.keras.datasets import mnist
from keras.datasets import mnist
import keras
import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score

# print(keras.__version__)
tv = tf.compat.v1

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# print(x_train.shape, y_train.shape)
# print(x_test.shape, y_test.shape)
# (60000, 28, 28) (60000,)
# (10000, 28, 28) (10000,)

x_train = x_train.reshape(x_train.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)

n = len(np.unique(y_train))

y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)

xp = tv.placeholder(tf.float32, shape = [None, 28*28])

w1 = tv.Variable(tv.random.normal([28*28, 64]), name='weight1')
b1 = tv.Variable(tv.zeros(64), name='bias1')
layer1 = tv.matmul(xp, w1) + b1

w2 = tv.Variable(tv.random.normal([64, n]), name='weight2')
b2 = tv.Variable(tv.zeros([n]), name='bias2')
hypothesis = tv.matmul(layer1, w2) + b2

yp = tv.placeholder(tf.float32, shape = [None, n])

loss = tf.reduce_mean(-tf.reduce_sum(yp*tf.nn.log_softmax(hypothesis), axis=1))
# loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=yp, logits=hypothesis))
train = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)
# loss= tf.losses.log_loss()

epochs = 500

sess = tv.Session()
sess.run(tv.global_variables_initializer())

for step in range(epochs):
    _, loss_val = sess.run([train, loss], feed_dict={xp:x_train, yp:y_train})
    y_pred = sess.run(hypothesis, feed_dict={xp:x_test})
    print(f'epoch : {step}\t\t{step*100/epochs}% complete\t\tloss : {loss_val}')
print('acc : ', accuracy_score(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1)))    
