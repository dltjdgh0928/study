import numpy as np
import matplotlib.pyplot as plt

f = lambda x : x**2 - 4*x + 6
# def f(x):
#     return x**2 - 4*x + 6

gradient = lambda x : 2*x - 4

x = -10.0       # 초기값
epochs = 20
learning_rate =0.9

a = []
b = []

for i in range(epochs):
    x = x - learning_rate * gradient(x)
    if i == 0:
        print(f'epoch\t x\t f(x)')
    print(f'{i+1:02d} \t{x:6.5f} \t{f(x):6.5f}')
    a.append(x)
    b.append(f(x))

a_index = np.argsort(a)
sorted_y = [b[i] for i in a_index]
a.sort()

plt.plot(a, sorted_y, 'k-')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()
