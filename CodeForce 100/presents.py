n = int(input(""))

# the fren sequence
s = [int(x) for x in input("").split(" ")]

# create an empty list with n values
o = [0] * n

for i in s:
    o[i-1] = s.index(i)+1

print(" ".join([str(x) for x in o]))