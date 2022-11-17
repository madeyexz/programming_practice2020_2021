import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.linear_model import LinearRegression

sizel = []
intervall = []

for size in range(1,10**4):
    sizel.append(size)
    # lst = [0] * size
    dct = dict(zip([x for x in range(size+1)],[0]*size))
    val = size // 2
    start = time.time()
    # get = dct[val]  # get
    del dct[val]
    end = time.time()
    interval = start - end
    intervall.append(interval)

plt.plot(intervall,sizel)
plt.xlabel('time (s)')
plt.ylabel('size of dict (in number of element pairs)')
plt.autoscale(True)
plt.grid(True)
plt.title('Relation of Size of Dict and Time Consumption of del[key]')

intervall_re = np.array(intervall).reshape((-1,1))
model = LinearRegression().fit(intervall_re, sizel)
lr = model.score(intervall_re, sizel)

print('coefficient of determination:' + str(lr))

plt.savefig("test.png")
plt.show()