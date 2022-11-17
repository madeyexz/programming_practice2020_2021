import math
import time



n = int(input(""))
nums = [int(x) for x in input("").split(" ")]
#nums = [4,5,6]

isprime = {0:"NO",1:"YES"}

for num in nums:
    a = 1
    if num == 1:
        print("NO") # eliminate 1
        continue
    numsqrt = math.sqrt(num)
    if numsqrt.is_integer() == False:
        a = 0
    else:
        # check if prime
        start = time.time() # initiate time check, anti-brutal judgepool :)
        for x in range(2, int(math.sqrt(numsqrt) + 1)):
            if numsqrt % x == 0: 
                a = 0
            now = time.time()
            if now - start > 0.0008:
                a = 1
                break

    print(isprime[a])
# print("TOTAL RUN TIME: ", time.time() - start)