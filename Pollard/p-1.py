import math

import numpy as np
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


def B1(num1, sieve_base):
    board = []
    for i in sieve_base:
        if i <= num1:
            k = i
            while k <= num1:
                k *= i
            else:
                board.append(k // i)
    return board


def M(num1):
    num1 = np.array(num1)
    return num1.prod()


def step_1(m, n, a):
    a_new = pow(a, int(m), n)
    print("a**M mod n", a_new)
    gcd = math.gcd(n, a_new - 1)
    if gcd == n:
        print("Замена а")
        step_1(m, n, a + 1)
    else:
        print("Стадия 1", gcd)
        return gcd, a_new


def step_2(n, num1, b, sieve_base):
    num2 = num1 ** 2
    q = []
    D = []
    res = []
    for i in sieve_base:
        if i > num1 and i < num2:
            q.append(i)

    for k in range(len(q) - 1):
        D.append(q[k + 1] - q[k])
        res.append(pow(b, D[k], n))
    print("Разность D", len(D), D)
    print("Степени числа b", len(res), res)

    c = pow(b, q[0], n)
    d = math.gcd(n, c - 1)
    k = 0
    while d == 1 and k < len(res):
        c = c * pow(b, res[k], n)
        d = math.gcd(n, c - 1)
        k += 1

    else:
        print("Стадия 2", d)
        return d


def solver(n, num1, a, sieve_base, res):
    if isPrime(n):
        res.append(n)
    else:
        b1 = B1(num1, sieve_base)
        print("Набор из произведения простых множителей", b1)
        m = M(b1)
        print("Общее произведение", m)
        factor, b = step_1(m, n, a)
        print("ff", factor, b)

        if factor != 1:
            solver(factor, num1, a, sieve_base, res)
            solver(n // factor, num1, a, sieve_base, res)
        elif factor == 1:
            factor = step_2(n, num1, b, sieve_base)
            solver(factor, num1, a, sieve_base, res)
            solver(n // factor, num1, a, sieve_base, res)

    return res


if __name__ == "__main__":
    res = []
    # n=672038771836751227845696565342450315062141551559473564642434674541
    n = 44381 * 40739
    a = 3
    print(solver(n, 13, a, sieve_base, res))
