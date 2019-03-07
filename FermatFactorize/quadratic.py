import math

import numpy as np
from ecdsa.numbertheory import jacobi
from sympy import Matrix

sieve_base = [2, 3, 5, 7, 11, 13, 17, 19,
              23, 29, 31, 37, 41, 43, 47, 53,
              59, 61, 67, 71, 73, 79, 83, 89,
              97, 101, 103, 107, 109, 113, 127, 131,
              137, 139, 149, 151, 157, 163, 167, 173,
              179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263,
              269, 271, 277, 281, 283, 293, 307, 311,
              313, 317, 331, 337, 347, 349, 353, 359,
              367, 373, 379, 383, 389, 397, 401, 409,
              419, 421, 431, 433, 439, 443, 449, 457,
              461, 463, 467, 479, 487, 491, 499, 503,
              509, 521, 523, 541, 547, 557, 563, 569,
              571, 577, 587, 593, 599, 601, 607, 613,
              617, 619, 631, 641, 643, 647, 653, 659,
              661, 673, 677, 683, 691, 701, 709, 719,
              727, 733, 739, 743, 751, 757, 761, 769,
              773, 787, 797, 809, 811, 821, 823, 827,
              829, 839, 853, 857, 859, 863, 877, 881,
              883, 887, 907, 911, 919, 929, 937, 941,
              947, 953, 967, 971, 977, 983, 991, 997]


def step_1(n, M):  # M - граница просеивания
    x = math.floor(math.sqrt(n)) + 1  # округление в меньшую сторону
    M = x + M
    arrX, arrY = [], []
    for xi in range(x, M + 1):
        y = math.sqrt(xi ** 2 - n)
        if math.floor(y) == math.ceil(y):  # если верхняя и нижняя границы равны, то .0 (точный квадрат)
            p, q = xi - math.floor(y), xi + math.floor(y)
            return p, xi ** 2 - n
        else:
            arrX.append(xi)  # запись для П(xi)
            arrY.append(xi ** 2 - n)  # запись для П(xi**2 - n)
    return arrX, arrY


def find_factor_base(n, B):  # через квадратичные вычеты , где B - граница факторной базы
    FB = [2]
    for p in sieve_base:
        if jacobi(p, n) == 1 and p <= B:
            FB.append(p)
    print("\nФакторная база: ", FB)
    return FB


def screening(arrX, arrY, FB):
    tempY = arrY.copy()
    resX = []
    resY = []
    powers = []
    for i in range(len(tempY)):
        tempPower = []  # список степеней
        for j in range(len(FB)):
            k = 0  # подсчет степеней
            while tempY[i] % FB[j] == 0:
                tempY[i] //= FB[j]
                k += 1
            tempPower.append(k)
        if tempY[i] == 1:
            resX.append(arrX[i])
            resY.append(arrY[i])
            powers.append(tempPower)
    return resX, resY, np.array(powers, dtype=np.int8).T % 2


"""
def solver(A):
    m, n = np.shape(A)
    used = []
    for r in range(m):
        used.append(0)

    for k in range(n):
        for r in range(m):
            if A[r, k] and not used[r]:
                for i in range(m):
                    if A[i, k] and r != i:
                        for j in range(n):
                            A[i, j] = (A[i, j] + A[r, j]) % 2
                used[r] = 1
    return A
"""


def find_p_q(n, arrX, arrY, vec):
    y = 1
    X = 1
    for i in range(len(vec)):
        if vec[i] == 1:
            y = y * arrY[i]
            X = X * arrX[i]
    y = int(math.sqrt(y))
    print("X = %s, y = %s, X - y = %s" % (X, y, X - y))
    return math.gcd(n, X - y)


def step_2(n, M, B):
    print("________________________\nФАКТОРИЗУЕМ %s\nграница просеивания M  = %s\nграница факторной базы B = %s" % (
        n, M, B))
    t1, t2 = step_1(n, M)
    if isinstance(t1, int):
        print("\nСреди чисел вида x**2 - n нашелся точный квадрат %s" % (t2))
        return t1, n // t1
    else:
        FB = find_factor_base(n, B)
        X, Y, powers = screening(t1, t2, FB)
        print("B-гладкие числа: ", Y)
        print("х-сы B-гладких чисел", X)
        print("Полученные степени:\n", powers)

        _, vec = Matrix(powers).rref()
        mx = abs(np.array(Matrix(powers).nullspace()))
        count, m = np.shape(mx)
        print("Найдено решений %s:\n%s\n" % (count, mx))
        if count != len(FB):
            for i in range(count):
                print("Решаем %s-е уравнение системы" % (i + 1))
                p = find_p_q(n, X, Y, mx[i])
                if (p == 0 or p == n) and count != 1:
                    print("Тривиальное решение: %s, %s\nПробуем другое решение\n" % (p, n // p))
                elif (p == 0 or p == n) and count == 1:
                    print("Тривиальное решение: %s, %s\nПопробуем увеличить границы\n" % (p, n // p))
                    return step_2(n, M + 30, B + 30)
                else:
                    print("Нетривиальные делители: %s, %s\n" % (p, n // p))
                    return p, n // p
        else:
            print("Решений не найдено, попробуем увеличить границы")
            step_2(n, M + 30, B + 30)


if __name__ == "__main__":
    print(step_2(112093, 30, 11))
    # print(step_2(97344, 40, 29))
    # print(step_2(364729, 40, 29))
