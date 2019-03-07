import math

from Crypto.Util.number import isPrime

def fermat(n, res):
    n=int(n)
    if isPrime(n):
        res.append(n)
    else:
        s = math.ceil(math.sqrt(n))
        print("Первый s ", s)
        sqr_sieve = []
        for i in range(0, s):
            sqr_sieve.append(i ** 2)
        print("квадраты ",sqr_sieve)

        #print("s", s, s ** 2, n, s ** 2 - n)
        while ((s ** 2 - n) not in sqr_sieve):  # до sqr_sieve размера
            s += 1
            #print("s", s, s ** 2, n, s ** 2 - n)
        y = int(math.sqrt(s ** 2 - n))
        print("s,y, s+y, s-y ",s, y, s+y, s-y,"\n")

        fermat(s + y, res)
        fermat(s - y, res)

    return res

if __name__ == "__main__":
    print("Введите число: n")
    n=input()
    res = []
    print("Факторизация ",fermat(n, res))
