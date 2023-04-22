import math
import cmath

def quadratic(a, b, c, d, e):
    P = (c ** 2 + 12 * a * e - 3 * b * d) / 9
    Q = (27 * a * d ** 2 + 2 * c ** 3 + 27 * b ** 2 * e - 72 * a * c * e - 9 * b * c * d) / 54
    D = cmath.sqrt(Q ** 2 - P ** 3)
    if abs(Q + D) >= abs(Q - D):
        u = cube_root(Q + D)
    else:
        u = cube_root(Q - D)
    if u == 0:
        v = 0
    else:
        v = P / u
    w = complex(-0.5, 3 ** 0.5 / 2)
    m = []
    M = []
    flag = 0
    roots = []
    for i in range(3):
        x = cmath.sqrt(b ** 2 - 8 * a * c / 3 + 4 * a * (w ** i * u + w ** (3 - i) * v))
        m.append(x)
        M.append(abs(x))
        if x == 0:
            flag = flag + 1
    if flag == 3:
        mm = 0
        S = b ** 2 - 8 * a * c / 3
        T = 0
    else:
        t = M.index(max(M))
        mm = m[t]
        S = 2 * b ** 2 - 16 * a * c / 3 - 4 * a * (w ** t * u + w ** (3 - t) * v)
        T = (8 * a * b * c - 16 * a ** 2 * d - 2 * b ** 3) / mm
    x1 = (-b - mm + cmath.sqrt(S - T)) / (4 * a)
    x2 = (-b - mm - cmath.sqrt(S - T)) / (4 * a)
    x3 = (-b + mm + cmath.sqrt(S + T)) / (4 * a)
    x4 = (-b + mm - cmath.sqrt(S + T)) / (4 * a)
    roots.append(x1)
    roots.append(x2)
    roots.append(x3)
    roots.append(x4)
    return roots

def cube_root(x):
    if x.imag == 0:
        m = x.real
        if m < 0:
            ans = -math.pow(-m, 1 / 3)
        else:
            ans = math.pow(m, 1 / 3)
    else:
        ans = x ** (1 / 3)
    return ans