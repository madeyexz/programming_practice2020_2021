n = int(input(""))
x = 0
for i in range(n):
    cmd = input("")
    if "++" in cmd:
        x += 1
    if "--" in cmd:
        x -= 1
print(x)