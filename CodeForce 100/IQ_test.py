n = int(input(""))
nums = [int(x) for x in input("").split(" ")]
nums_1 = []
for i in nums:
    nums_1.append(i%2)
even, odd = nums_1.count(0), nums_1.count(1)

if even > odd: # find the odd
    print(nums_1.index(1)+1)
else: # find the even
    print(nums_1.index(0)+1)
