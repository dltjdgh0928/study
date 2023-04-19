import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA

# 1. 데이터
x, y = load_digits(return_X_y=True)
print(x.shape)      # (1797, 64)

# pca = PCA(8)
# x = pca.fit_transform(x)
# print(x.shape)      # (1797, 8)

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=337)

# scaler = MinMaxScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.transform(x_test)

# 2. 모델
# model = RandomForestClassifier()
# model = make_pipeline(MinMaxScaler(), RandomForestClassifier())
# model = make_pipeline(StandardScaler(), RandomForestClassifier())
model = make_pipeline(PCA(8), StandardScaler(), SVC())

# 3. 훈련
model.fit(x_train, y_train)

# 4. 평가, 예측
result = model.score(x_test, y_test)
print('model.score : ', result)

y_pred = model.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print('acc : ', acc)