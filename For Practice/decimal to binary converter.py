import random


pwd = ""
for i in range (63):
    pwd += str(random.randint(0,9))

print(pwd)
    