import time

start = time.time()


def primes_sieve1(n = 1000000000000):
    n1 = n+1
    primes = dict()
    for i in range(2, n1): primes[i] = True

    for i in primes:
        factors = range(i,n1, i)
        for f in factors[1:]:
            primes[f] = False
    
    return [i for i in primes if primes[i]==True]

primes = primes_sieve1()
print("Time used generating prime list: ", time.time() - start)

n = int(input(""))

nums = [int(x) for x in input("").split(" ")]
for num in nums:
    print("YES" if num in primes else "NO")
    # n = int(input(""))
    # prime_list = []
    # real_list= []
    # for i in range(2, n+1):
    #     if i not in prime_list:
    #         real_list.append(i)            
    #     for j in range(i*i, n+1, i):
    #         prime_list.append(j)
    # print("YES" if n in real_list else "NO")

# print("Total run time: ", time.time() - start)