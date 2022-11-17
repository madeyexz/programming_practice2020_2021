all = [int(x) for x in input('').split(' ')]
yes = []
no = []

for item in all:
    if item > 0:
        yes.append(item)
    else:
        no.append(item)
    
print(no + yes)