a,b = map(int,input("").split(" "))
yr = 0
while b > a or a == b:
    a = 3*a
    b = 2*b
    yr += 1
print(yr)