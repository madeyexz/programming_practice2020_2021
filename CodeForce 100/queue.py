a = input("").split(" ")
n, t = int(a[0]), int(a[1])

s = input("")

for i in range(t):
    if "BG" in s:
        s = s.replace("BG", "GB", -1)
print(s)