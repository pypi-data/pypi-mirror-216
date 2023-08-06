def something():
    return None

def Q_update(Q, gamma):
    Q_k = Q[-1]
    Q_new = np.zeros((1, 2, 6))
    for s in range(6):
        for i, a in enumerate(["C", "M"]):
            summation = 0
            for s_prime in range(6):
                summation += T(s, a, s_prime) * (R(s, s_prime) + gamma * np.max(Q_k[:, s_prime]))
            Q_new[0, i, s] = summation
    Q = np.concatenate((Q, Q_new))
    return Q

Q = np.zeros((1, 2, 6))
gamma = 0.6
print(np.argmax(Q_update(Q, gamma)[-1], axis = 0))
def add_one(number):
    return number + 1

def minus_one(number):
    return number - 1

def multiplication(number1, number2):
    return number1 * number2