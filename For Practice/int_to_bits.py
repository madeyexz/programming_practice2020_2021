def count_bits(n):
    n = "{0:b}".format(n)
    c = 0
    for i in n:
        if i == "1":
            c += 1
    return c

print(count_bits(10))