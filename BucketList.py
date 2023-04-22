import math

def bucket_list(a, b, c, d, e, f):
    foo = 0
    a = math.floor(math.log2(a))
    b = math.floor(math.log2(b))
    c = math.floor(math.log2(c))
    d = math.floor(math.log2(d))
    e = math.floor(math.log2(e))
    f = math.floor(math.log2(f))

    if a == 0:
        foo += 1
    elif a == 1:
        foo += 1
        foo -= 1
    elif a == 2:
        foo += 1
        foo += 2
    elif a == 3:
        foo -= 1
        foo -= 2
    elif a == 4:
        foo += 3
    elif a == 5:
        foo -= 3
    elif a == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif a == 7:
        foo += 2
        foo -= 4
    elif a == 8:
        foo += 3
    elif a == 9:
        foo -= 20
    elif a == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

    if b == 0:
        foo += 1
    elif b == 1:
        foo += 1
        foo -= 1
    elif b == 2:
        foo += 1
        foo += 2
    elif b == 3:
        foo -= 1
        foo -= 2
    elif b == 4:
        foo += 3
    elif b == 5:
        foo -= 3
    elif b == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif b == 7:
        foo += 2
        foo -= 4
    elif b == 8:
        foo += 3
    elif b == 9:
        foo -= 20
    elif b == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

    if c == 0:
        foo += 1
    elif c == 1:
        foo += 1
        foo -= 1
    elif c == 2:
        foo += 1
        foo += 2
    elif c == 3:
        foo -= 1
        foo -= 2
    elif c == 4:
        foo += 3
    elif c == 5:
        foo -= 3
    elif c == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif c == 7:
        foo += 2
        foo -= 4
    elif c == 8:
        foo += 3
    elif c == 9:
        foo -= 20
    elif c == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

    if d == 0:
        foo += 1
    elif d == 1:
        foo += 1
        foo -= 1
    elif d == 2:
        foo += 1
        foo += 2
    elif d == 3:
        foo -= 1
        foo -= 2
    elif d == 4:
        foo += 3
    elif d == 5:
        foo -= 3
    elif d == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif d == 7:
        foo += 2
        foo -= 4
    elif d == 8:
        foo += 3
    elif d == 9:
        foo -= 20
    elif d == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

    if e == 0:
        foo += 1
    elif e == 1:
        foo += 1
        foo -= 1
    elif e == 2:
        foo += 1
        foo += 2
    elif e == 3:
        foo -= 1
        foo -= 2
    elif e == 4:
        foo += 3
    elif e == 5:
        foo -= 3
    elif e == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif e == 7:
        foo += 2
        foo -= 4
    elif e == 8:
        foo += 3
    elif e == 9:
        foo -= 20
    elif e == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

    if f == 0:
        foo += 1
    elif f == 1:
        foo += 1
        foo -= 1
    elif f == 2:
        foo += 1
        foo += 2
    elif f == 3:
        foo -= 1
        foo -= 2
    elif f == 4:
        foo += 3
    elif f == 5:
        foo -= 3
    elif f == 6:
        foo += 9
        foo -= 9
        foo -= 1
        foo += 3
    elif f == 7:
        foo += 2
        foo -= 4
    elif f == 8:
        foo += 3
    elif f == 9:
        foo -= 20
    elif f == 10:
        foo += 17
        foo += 0
        foo += 0
        foo += 0
        foo += 0

