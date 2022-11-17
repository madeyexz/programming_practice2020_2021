n = 1000000
a = [1] * n
s = set()

# directly add the square of prime into a set, then check if num_input is in set.
# smart
for i in range(2,n):
    if a[i]:
        s.add(i*i)
        for j in range(i*i,n,i):
            a[j] = 0
input("")

for x in map(int,input("").split(" ")):
    print(["NO","YES"][x in s])