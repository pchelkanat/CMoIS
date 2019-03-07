import math
import random

import numpy as np
import sympy
from Crypto.Util.number import isPrime

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


def M(n):
    # M = L(n)
    # L(n) = exp( sqrt(ln n * ln ln n))
    M = math.floor(math.sqrt(math.exp(math.sqrt(math.log(n, math.e) * math.log(math.log(n, math.e), math.e)))))
    print("M", M)
    return M


def factor_base(M):
    FB = []
    for i in sieve_base:
        if i <= M:
            FB.append(i)
        else:
            break
    return FB


def alphas(FB, a):
    alpha = []
    for i in range(len(FB)):
        power = 0
        while a % FB[i] == 0:
            a = a // FB[i]
            power += 1
        alpha.append(power)
    return alpha, a


def table(FB, r, n):
    eps = {}
    inds = {}
    b_list = {}
    i = 0
    print("Считаем от b = %s, до k = %-3s c фактор. базой %s" % (r, len(FB) + 1, FB))
    for b in range(r, n):
        a = b ** 2 % n
        alpha, new_a = alphas(FB, a)
        if new_a == 1:
            inds[i] = b
            b_list[b] = a
            eps[a] = alpha
            print("b%-3s = %-10s a = b**2 mod n = %-10s с разложением %s" % (i, b, a, alpha))
            i += 1
            if len(eps) == len(FB) + 1:  # пока не найдется h+1 значений. h - длина факторной базы
                break
    return inds, b_list, eps


def table2(FB, r, n):
    eps = {}
    inds = {}
    b_list = {}
    print("Считаем от b = %s, до k = %-10s c фактор. базой %s" % (r, len(FB) + 1, FB))
    i=0
    while i!=len(FB) + 1:
        b = random.randrange(r, n)
        a = b ** 2 % n
        alpha, new_a = alphas(FB, a)
        if new_a == 1:
            inds[i] = b
            b_list[b] = a
            eps[a] = alpha
            print("b%-3s = %-10s a = b**2 mod n = %-10s с разложением %s" % (i, b, a, alpha))
            i+=1

    return inds, b_list, eps


def depended_vectors(matrix):
    res = []
    for i in range(0, np.shape(matrix)[0] - 1):
        for j in range(i + 1, np.shape(matrix)[0]):
            temp = (matrix[i] + matrix[j]) % 2
            if temp.any() == 0:
                res.append([i, j])
    return res


def solving(n, inds, b_list, eps):
    print("Введите векторы, которые хотите проверить:")
    v1, v2 = input().split()
    b1 = inds[int(v1)]
    b2 = inds[int(v2)]
    a1 = b_list[b1]
    a2 = b_list[b2]

    print("\nЧисла b:\n%s, %s" % (b1, b2))
    print("\nЧисла a:\n%-5s с разложением %s\n%-5s с разложением %s" % (a1, eps[a1], a2, eps[a2]))

    x = b1 * b2 % n
    y = int(math.sqrt(a1 * a2) % n)
    print("\nНайдены:\nx = b1 * b2 mod n = %s,\ny = sqrt(a1 * a2) mod n = %s" % (x, y))

    if (x != y % n or x != -y % n):
        u = math.gcd(x + y, n)
        if u == n or u == 1:
            print("\nВЫБЕРЕТЕ ДРУГИЕ ВЕКТОРЫ-2 n = %s, u = %s!!!" % (n, u))
            solving(n, inds, b_list, eps)
        else:
            print("Найдены u = %s v = %s" % (u, n // u))
            return u, n // u
    else:
        print("\nВЫБЕРЕТЕ ДРУГИЕ ВЕКТОРЫ!!!")
        solving(n, inds, b_list, eps)


def dixon(n, res):
    print("-------------\nФАКТОРИЗУЕМ:", n)
    if isPrime(n) or n == 1:
        res.append(n)
    else:
        FB = factor_base(M(n))
        #FB = sieve_base[:10]
        r = math.ceil(math.sqrt(n))
        inds, b_list, eps = table(FB, r + 1, n)

        mx = np.mat(list(eps.values())).T % 2
        reduced_mx, independ = sympy.Matrix(mx).rref()
        print("\nИмеем матрицу:\nстроки - степени, столбцы - числа-векторы.")
        print(mx)
        print("\nПреобразованная матрица:")
        print(np.mat(reduced_mx))
        # print(sc.null_space(np.mat(reduced_mx)))

        red = np.mat(reduced_mx).T
        vec = depended_vectors(red)
        print("Линейно независимые векторы-столбцы %s" % ([independ]))
        print("Линейно зависимые векторы-столбцы %s" % (vec))

        u, v = solving(n, inds, b_list, eps)
        dixon(u, res)
        dixon(v, res)
    return res


if __name__ == "__main__":
    # print("Введите число: n")
    # n=input()
    res = []
    print("-------------\nФакторизация:", dixon(44381*40739, res))
    #print("-------------\nФакторизация:", dixon(40087*58477,res))
    #print("-------------\nФакторизация:", dixon(156307*249367], res))
