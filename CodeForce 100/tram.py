n = int(input(""))
capacity = 0
capacity_max = 0
for i in range(n):
    s = input("")
    a,b = int(s.split(" ")[0]), int(s.split(" ")[1])
    capacity = capacity - a + b
    if capacity > capacity_max:
        capacity_max = capacity
print(capacity_max)