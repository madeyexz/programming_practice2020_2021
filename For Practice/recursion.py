# # fibonacci sequence with recursion (with/without memoisation)
# import time


# this is a REC approach
def REC_fibonacci(n):
    if n == 1 or n == 0: # this is the base
        return n
    else:
        return REC_fibonacci(n-1) + REC_fibonacci(n-2) # top-down
    # n --> base

# this is a DP approach
memo = []*1000000
def DP_fibonacci(n):
	memo[0], memo[1] = 0, 1 # this is the base
	for i in range(2, n+1):
		memo[i] = memo[i-1] + memo[i-2] # bottom-up
	return memo[n]
    # base --> n