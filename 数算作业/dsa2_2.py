# 做计时实验，验证Dict的get item和set item都是O(1)的
# 做计时实验，验证List的按索引取值确实是O(1)
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.linear_model import LinearRegression


# 构造小的list，取值，构造大的list，取值，比较时间
sizel = []
intervall = []

for size in range(1,10**4):
    sizel.append(size)
    # lst = [0] * size
    dct = dict(zip([x for x in range(size+1)],[0]*size))
    val = size // 2
    start = time.time()
    # get = dct[val]  # get
    dct[size+1]=0
    end = time.time()
    interval = start - end
    intervall.append(interval)

plt.plot(intervall,sizel)
plt.xlabel('time (s)')
plt.ylabel('size of dict (in number of element pairs)')
plt.autoscale(True)
plt.grid(True)
plt.title('Relation of Size of Dict and Time Consumption of setitem')

intervall_re = np.array(intervall).reshape((-1,1))
model = LinearRegression().fit(intervall_re, sizel)
lr = model.score(intervall_re, sizel)

print('coefficient of determination:' + str(lr))

plt.savefig("test.png")
plt.show()