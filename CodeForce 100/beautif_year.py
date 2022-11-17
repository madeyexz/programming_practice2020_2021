year = int(input(""))
status = True

while status:
    year += 1
    if len(set(str(year))) == 4:
        status = False

print(year)