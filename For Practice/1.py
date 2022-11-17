# 用 2d list 记录三角形，然后从倒数第二排开始更改，将每个数改成下面 两个可以加上的数的最大和，就能往上推出最大路径。

n = int(input())
triangle=[]
ans=0

for i in range(n):
    triangle.append(list(map(int,input().split()))+[0 for j in range(n-i-1)])

for i in range(n-2,-1,-1):
    for j in range(i+1):
        triangle[i][j] += max( triangle[i+1][j] ,triangle[i+1][j+1] )

print(triangle[0][0])