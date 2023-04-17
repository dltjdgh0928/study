import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score


# 1. 데이터
x, y = load_iris(return_X_y=True)

# x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=123, shuffle=True)

n_split = 5
kf = KFold(n_splits=n_split, shuffle=True, random_state=123)
# kf = KFold()

# 2. 모델
model = LinearSVC(max_iter=100000)

# 3, 4. 컴파일, 훈련, 평가, 예측
scores = cross_val_score(model, x, y, cv=kf)
print(scores)

print('ACC : ', scores, '\n mean of cross_val_score : ', round(np.mean(scores), 4))
