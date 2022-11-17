i = [int(x) for x in input("").split(" ")]
bulbs_program = [int(x) for x in input("").split(" ")]
n, M = i[0],i[1]

# complete the bulb program in terms of head and tail
bulbs_program.append(M)
bulbs_program.append(0)
bulbs_program = sorted(bulbs_program)

# calc abs(bulbs_program[i] - bulbs_program[i-1]) and append to lst abs_interval
# a = sum(abs_interval[::2])
# update a for each loop
# print a

a = 0 # maximal lit interval

for extra in range(M):
    temp_program = []
    temp_program.extend(bulbs_program)
    temp_program.append(extra)
    temp_program = list(set(sorted(temp_program)))
    abs_interval = []
    for j in range(1, len(temp_program)):
        abs_interval.append(temp_program[j]-temp_program[j-1]) # did not use abs() bc there is no need, call it interval will be fine
    if sum(abs_interval[::2]) > a:
        a = sum(abs_interval[::2])
print(a)