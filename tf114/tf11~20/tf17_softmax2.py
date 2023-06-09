import tensorflow as tf
import numpy as np
from sklearn.metrics import r2_score, accuracy_score
tf.compat.v1.set_random_seed(337)

x_data = [[1, 2, 1, 1],
          [2, 1, 3, 2],
          [3, 1, 3, 4],
          [4, 1, 5, 5],
          [1, 7, 5, 5],
          [1, 2, 5, 6],
          [1, 6, 6, 6],
          [1, 7, 6, 7]]

y_data = [[0, 0, 1],
         [0, 0, 1],
         [0, 0, 1],
         [0, 1, 0],
         [0, 1, 0],
         [0, 1, 0],
         [1, 0, 0],
         [1, 0, 0]]

# 2. 모델구성
x = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])
w = tf.compat.v1.Variable(tf.random.normal([4, 3]), name='weight')
b = tf.compat.v1.Variable(tf.zeros([1, 3]), name='bias')
y = tf.compat.v1.placeholder(tf.float32, shape=[None, 3])

hypothesis = tf.compat.v1.matmul(x, w) + b

# 3-1 컴파일
loss = tf.reduce_mean(-tf.reduce_sum(y*tf.nn.log_softmax(hypothesis), axis=1))

# loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=hypothesis))
train = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=1e-5).minimize(loss)

# 3-2. 훈련
epochs = 1000
with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())    
    for step in range(epochs):
        _, loss_val, w_val, b_val = sess.run([train, loss, w, b], feed_dict={x:x_data, y:y_data})
    
    # 4. 평가, 예측
    xp2 = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])
    y_pred = tf.nn.softmax(tf.compat.v1.matmul(xp2, w_val) + b_val)
    y_predict = sess.run([y_pred], feed_dict={xp2:x_data})
    print('acc : ', accuracy_score(np.argmax(y_data, axis=1), np.argmax(y_predict[0], axis=1)))



