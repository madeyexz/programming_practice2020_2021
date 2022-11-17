def wheat_from_chaff(lst):

    fpos = lst.index([x for x in lst if x > 0][0]) # fpos = index of fpos
    lneg = lst.index([x for x in lst if x < 0][-1]) # lneg = index of lneg

    if fpos - lneg == 1:
        return lst
    
    else:
        lst[fpos],lst[lneg] = lst[lneg],lst[fpos]
        return wheat_from_chaff(lst)

# i = [int(x) for x in input('').split(' ')]

i = [-46,-50,-28,-45,-27,-40,10,35,34,47,-46,-24]
print(wheat_from_chaff((i)))