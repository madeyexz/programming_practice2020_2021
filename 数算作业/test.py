import random
import os
lst = []
for i in range(100):
    lst.append(random.randint(1,100000))
os.system('echo %s | pbcopy' % (str(lst)))

