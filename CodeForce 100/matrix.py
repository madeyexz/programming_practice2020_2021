a = ""
for i in range(5):
    a += input("")
    a += "\n"

rows = a.split('\n')

for i in rows:
    if "1" in i:
        ix, iy = rows.index(i)+1, i.index("1")-i[0:i.index("1")+1].count("0")+1

print(abs(3-ix)+abs(3-iy))