n = int(input("")) # number of coins == len(s)
s = sorted(list(map(lambda x: int(x), input("").split(" "))),reverse = True) # sequence of coins

for i in range(n):
    if sum(s[:i]) > sum(s[i:]):
        print(i)
        break
    
    elif n == 2 and s[0] == s[1]:
        print(n)
        break

    elif n == 1:
        print(1)
        break