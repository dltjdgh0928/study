import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.svm import SVC

# 1. 데이터
x, y = load_iris(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=337)

parameters =[
    {'rf__n_estimators':[100, 200], 'rf__max_depth':[6,8,10], 'rf__min_samples_leaf':[1,10]}, 
    {'rf__max_depth':[6,8,10,12], 'rf__min_samples_leaf':[3,5,7,10]},
    {'rf__min_samples_leaf':[3,5,7,10], 'rf__min_samples_split':[2,3,5,10]},
    {'rf__min_samples_split':[2,3,5,10]},
    {'rf__n_jobs':[-1, 2, 4], 'rf__min_samples_split':[2,3,5,10]}
]
# 2. 모델
pipe = Pipeline([('std', StandardScaler()), ('rf', RandomForestClassifier())])

model = GridSearchCV(pipe, parameters, cv=5, verbose=1)

# 3. 훈련
model.fit(x_train, y_train)

# 4. 평가, 예측
result = model.score(x_test, y_test)
print('model.score : ', result)

y_pred = model.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print('acc : ', acc)