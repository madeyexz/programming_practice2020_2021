cor = [int(x) for x in input("").split(" ")]

mid = sum(cor) // 3
dis = max(cor) - min(cor)

for j in range(min(cor),max(cor)+1):
    a = 0
    for i in cor:
        a += abs(j - i)
    if a < dis:
        dis = a

print(dis)