import math


num = 3

while True:
    isprime = True
    
    for x in range(2, int(math.sqrt(num) + 1)):
        if num % x == 0: 
            isprime = False
            break
    
    if isprime:
        print(num, end = " ")
    
    num += 1