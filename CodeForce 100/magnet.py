n = int(input())
a = []
count = 1
for i in range(n):
    a.append(input())
    if a[i] != a[i-1]:
        count += 1
print(count)
# hahaha