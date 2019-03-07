def egcd(a, b):
    x, x1 = 1, 0
    y, y1 = 0, 1
    while b:
        q = a // b
        x, x1 = x1, x - q * x1
        y, y1 = y1, y - q * y1
        a, b = b, a - q * b
    return a, x, y


def index(g, t, p):
    a, b, x = [0], [0], [1]
    xi = 0
    xj = 0
    print("i=%s a=%s b=%s x=%s" % (0, a[0], b[0], x[0]))
    for i in range(1, p):
        if 0 < x[i - 1] < p / 3:
            a.append((a[i - 1] + 1) % (p - 1))
            b.append(b[i - 1] % (p - 1))
            temp = t * x[i - 1] % p
            x.append(temp)
            print("i=%s a=%s b=%s x=%s" % (i, a[i], b[i], x[i]))
            if i % 2 == 0:
                #print("a=%s b=%s x=%s || a=%s b=%s x=%s" % (a[i],b[i], x[i], a[i//2],b[i//2],x[i//2]))
                if x[i] == x[i // 2]:
                    xi = x.index(temp)
                    xj = i
                    break

        elif p / 3 < x[i - 1] < 2 * p / 3:
            a.append(2 * a[i - 1] % (p - 1))
            b.append(2 * b[i - 1] % (p - 1))
            temp = x[i - 1] ** 2 % p
            x.append(temp)
            print("i=%s a=%s b=%s x=%s" % (i, a[i], b[i], x[i]))
            if i % 2 == 0:
                if x[i] == x[i // 2]:
                    xi = x.index(temp)
                    xj = i
                    break

        elif 2 * p / 3 < x[i - 1] < p:
            a.append(a[i - 1] % (p - 1))
            b.append((b[i - 1] + 1) % (p - 1))
            temp = g * x[i - 1] % p
            x.append(temp)
            print("i=%s a=%s b=%s x=%s" % (i, a[i], b[i], x[i]))
            if i % 2 == 0:
                if x[i] == x[i // 2]:
                    xi = x.index(temp)
                    xj = i
                    break
    print()
    return a, b, x, xi, xj


def ro(g, t, p):
    g, t, p = int(g), int(t), int(p)
    a, b, x, xi, xj = index(g, t, p)
    print("xi = %s, xj = %s\nx[xi] = %s, x[xj] = %s" % (xi, xj, x[xi], x[xj]))

    A, B = a[xj] - a[xi], p - 1
    gcd, X, Y = egcd(A, B)
    if X < 0:
        X, Y = Y, X
    print("gcd = %s, X = %s, Y = %s" % (gcd, X, Y))

    if gcd == 1:
        k = X % (p - 1)
        k2 = ((b[xi] - b[xj]) / A) % (p - 1)
        print("k1 = %s, k2 = %s" % (k, k2))
        print("result %s ** %s mod %s = %s" % (g, k, p, g ** k % p))
    else:
        x0 = X * gcd # like  gcd*(Ax+By=1) = Ax*gcd + By*gcd = gcd
        d = (p - 1) // gcd
        print("x0 = %s, d = %s => k = %s + %sm" % (x0, d, x0, d))

        for m in range(gcd):
            k = x0 + m * d
            if (g ** k) % p == t:
                print("m = %s, k = %s" % (m,k))
                print("result %s**%s mod %s = %s" % (g, k, p, g ** k % p))

if __name__=="__main__":
    print("Введите числа: a, b, mod n:")
    a, b, mod = input(), input(), input()
    ro(a, b, mod)
