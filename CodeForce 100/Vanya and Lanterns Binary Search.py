n, l = [int(x) for x in input().split(" ")]
pos = sorted([int(x) for x in input().split(" ")],reverse = True)
max_int = 0
for i in range(1,len(pos)):
    a = abs(pos[i-1] - pos[i])
    if a > max_int:
        max_int = a

if ((max_int / 2) > (l - pos[0])) and ((max_int / 2) > pos[-1]):
    print(max_int / 2)
else:
    print(max((l - pos[0]), (pos[-1])))