import math

# number of groups
ng = int(input(""))

# group sequence, make item in sequence int
# gs = list(map(lambda x:int(x), input("").split(" ")))

a,b,c,d = map(input("").count, ("1","2","3","4"))

taxi = 0
taxi += d+c+math.ceil((max(a-c,0)+2*b)/4)

print(int(taxi))