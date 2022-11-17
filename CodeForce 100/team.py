round = int(input(""))

agreed_solution_count = 0

for i in range(round):
    choices = input("")
    count = 0
    for j in choices:
        if j == "1":
            count += 1
    if count > 1:
        agreed_solution_count += 1
print(agreed_solution_count)