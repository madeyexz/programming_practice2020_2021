i = [int(x) for x in input("").split(" ")]
n_butt, n_bulb = i[0], i[1]

# initiate the light bulbs
bulbs = [0] * n_bulb

for rounds in range(n_butt):
    j = [int(x) for x in input("").split(" ")]
    total_bulbs_lit_this_round = j[0]
    position_series_of_bulb = j[1:]

    for position in position_series_of_bulb:
        bulbs[position-1] = 1

print(["YES","NO"][0 in bulbs])