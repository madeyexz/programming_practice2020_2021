import math
m,n,a = input("").split(" ")
def cover(m, n, a):
    m = int(m)
    n = int(n)
    a = int(a)
    print(int(math.ceil(m/a)*math.ceil(n/a)))

cover(m,n,a)