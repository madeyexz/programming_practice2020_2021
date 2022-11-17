from collections import defaultdict
# import sys

c = int(input(""))

# case loop
for case in range(c):
    a = 0
    n,m,b = [int(x) for x in input().split(" ")]
    ability = defaultdict(list)

    # create ability dictionary {ti:[xi]}
    for i in range(n):
        t,x = [int(x) for x in input().split(" ")]
        if t > a:
            a = t
        ability[t].append(x)
    
    # sort value list by damage in descending order
    for key in ability:
        ability[key] = sorted(ability[key], reverse = True)
    
    for t in sorted(ability):
        if m >= len(ability[t]):
            b = b - sum(ability[t])
        else:
            b = b - sum(ability[t][:m])
        if b <= 0:
            print(t)
            break
    if b > 0:
        print('alive')
#    print(sys.getsizeof(ability))
# for each case
# store TIME-list(DAMAGE) pair in a dictionary
# sort the value of each pair in desending order
# for t in range(1, max(sorted(ability)) + 1):
#   b - sum of the first M ABILITY,
#   if b < 0:
#       print(t)
#       break
# if b > 0:
# print('alive')