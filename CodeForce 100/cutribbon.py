# ax + by + cz = n
# find the maximum value of sum(x,y,z)
# a mathematical approach



# Idea Behind:
# 1. suppose we have 0 ribbon at present
# 2. now we cut length i, if i equals a,b or c, we now have 1 ribbon (+1)
# 3. now we cut another length l, if l equals a,b or c, we now have 2 ribbons (1+1)
# 4.1 To generalize it, we find that whenever we cut length a,b or c, we obtain another piece of ribbon, and the maximum pieces of ribbon is the previously maximum pieces + 1
# 4.2 Before we take another cut, the original maximum piece contains in either index[i-a], index[i-b] or index[i-c],
# 4.3 Therefore 'sheet[index] = max(sheet[index-a],sheet[index-b],sheet[index-c]) + 1'

n,a,b,c = [int(x) for x in input('').split(' ')]
# creating the answer sheet (list), [0] marks the start
sheet = [0] + [-1000] * 4000

# iterates from 1 to n+1, if we start from index 0, the original sheet[0] = 0 will be replaced by -1000
# making the sheet unusable, stops at index[n+1] because we want to cover index[n]
for index in range(1,n+1):
    sheet[index] = max(sheet[index-a],sheet[index-b],sheet[index-c]) + 1
    # the '+1' at the end of line marks the reception of ribbon

print(sheet[n])