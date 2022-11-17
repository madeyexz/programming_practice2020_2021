treasure = [{'w':2,'v':3},{'w':3,'v':4},{'w':4,'v':8},{'w':5,'v':8},{'w':9,'v':10}]
maxw = 20

#TODO要求写算法输出选取最高总价值的宝物的序号以及价值

# dynamic programming - How to be a Proficient Robber
# let W be the maximum weight, let Y <= W
# let A(Y) be the maximum value under maximum weight Y, thus A(W) is the answer
# now we want to make a list of A(Y) forall Y in [1,W]
# A(Y) = max{ A(Y-1), pj+A(Y-wj) }, where (pj,wj)=(value of j, weight of j)

def how_to_be_a_proficient_robber(treasure=treasure,maxw=maxw):
    treasure.insert(0,{'w':0,'v':0})
    w = [x['w'] for x in treasure]
    v = [x['v'] for x in treasure]
    maxw = 20
    dp = [[0 for i in range(maxw+1) ]for i in range(len(w))]
    for i in range(len(w)):
        for j in range(maxw+1):
            if j < w[i]:
                    dp[i][j] = dp[i-1][j]
            else:
                    dp[i][j] = max(dp[i-1][j], dp[i-1][j-w[i]] + v[i])
    for i in dp:
        print(i)
        
    j=maxw
    for i in reversed(range(1, len(treasure)+1)):
        if dp[j][i] > dp[j][i-1]:
            treasurelist.append(i-1)
            j -= treasure[i-1]['w']

    treasurelist.reverse()
    return dp[-1][-1],treasurelist

print(how_to_be_a_proficient_robber())