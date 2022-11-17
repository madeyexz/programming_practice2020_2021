import time
import random
import os

os.system("clear")
pw = input("Enter your password: ")
os.system("clear")

pw = str(pw)

init = "initiating password breaking"
print(init, end = "")
for i in range(7):
    time.sleep(0.2)
    print(".", end = "")


ri = ""

for i in range(40):
    for j in range(2000):
        ri += str(random.randint(0,9))
    time.sleep(0.05)
    os.system("clear")
    print(ri)
    ri = ""

os.system("clear")

time.sleep(0.2)
print("Your password is: %s" % pw)