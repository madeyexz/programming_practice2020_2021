import time
start = time.time()

for i in range(int(input(""))):
    a = [int(x) for x in input("").split(" ")]
    dividend, divisor = a[0],a[1]

    if dividend % divisor == 0:
        print(0)
    else:
        if dividend > divisor:
            print(dividend % divisor)
        else:
            print(divisor - dividend)

print(time.time() - start)