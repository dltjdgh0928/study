import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, VotingClassifier

# 1. 데이터
x, y = load_breast_cancer(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=123, train_size=0.8, shuffle=True, stratify=y)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 2. 모델
lr = LogisticRegression()
knn = KNeighborsClassifier()
dt = DecisionTreeClassifier()

model = VotingClassifier(
    estimators=[('LR', lr), ('KNN', knn), ('DT', dt)],
    voting='hard'
)

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

# 4. 평가, 예측
print('score : ', model.score(x_test, y_test))
print('acc : ', accuracy_score(y_test, y_pred))

classifiers = [lr, knn, dt]
for model2 in classifiers:
    model2.fit(x_train, y_train)
    y_predict = model2.predict(x_test)
    score2 = accuracy_score(y_test, y_predict)
    class_name = model2.__class__.__name__
    print('{0} 정확도 : {1:.4f}'.format(class_name, score2))