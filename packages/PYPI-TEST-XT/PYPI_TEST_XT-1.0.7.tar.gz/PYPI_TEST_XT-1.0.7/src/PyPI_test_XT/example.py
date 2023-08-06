def add_one(number):
    return number + 1

def minus_one(number):
    return number - 1

def multiplication(number1, number2):
    return number1 * number2

import numpy as np
import math

# theta = np.array([0.0, 0.0])
# theta_0 = 0.0
#
# X = [[0, 0], [2, 0], [3, 0], [0, 2], [2, 2], [5, 1], [5, 2], [2, 4], [4, 4], [5, 5]]
# Y = [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
# mistakes = np.zeros((10, ))
# i = 0
# X = np.array(X[i:] + X[:i])
# Y = np.array(Y[i:] + Y[:i])
#
# for i in range(20):
#     for j in range(10):
#         if Y[j] * (theta @ X[j] + theta_0) <= 0:
#             theta += Y[j] * X[j]
#             theta_0 += Y[j]
#             mistakes[j] += 1
#
# from sklearn import svm
# clf = svm.SVC(kernel="linear", C=100000000000000000000)
# clf.fit(X, Y)
# theta = clf.coef_[0]
# theta_0 = clf.intercept_
# # print(theta)
# # print(theta_0)
#
#
# for i in range(10):
#     margin = Y[i] * (theta @ X[i] + theta_0) / (theta @ theta)**(0.5)
#     # print(margin)
#
#
# def hinge(val):
#     if val >= 1:
#         return 0
#     else:
#         return 1 - val
#
# val = []
# for i in range(10):
#     val.append(Y[i] * ((theta / 2) @ X[i] + (theta_0 / 2)))
# print(val)
# print(sum(list(map(hinge, val))))

X = [[0, 0],
     [2, 0],
     [1, 1],
     [0, 2],
     [3, 3],
     [4, 1],
     [5, 2],
     [1, 4],
     [4, 4],
     [5, 5]]
def phi(x):
    return [x[0]**2, math.sqrt(2) * x[0] * x[1], x[1]**2]

theta = np.zeros((1, 3))
theta_0 = 0
X = list(map(phi, X))
X = np.array(X)
y = [-1] * 5 + [1] * 5
y = np.array(y)
mistake = [1, 65, 11, 31, 72, 30, 0, 21, 4, 15]
yX = np.zeros((10, 3))
for i in range(10):
     yX[i] = y[i] * X[i]
theta += np.matmul(np.array(mistake).reshape(1, 10), yX).reshape(1, 3)
# print(theta)
theta_0 += np.array(mistake) @ y
# print(theta_0)

for i in range(10):
     print(y[i] * (theta @ X[i] + theta_0))
     if y[i] * (theta @ X[i] + theta_0) <= 0:
          print("False")

def Hello_World():
    print("Hello World")

def Happy_day():
    print("Happy day")