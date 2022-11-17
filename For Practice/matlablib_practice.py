import matplotlib.pyplot as plt
import numpy as np

arr_x = np.arange(0,10,0.01)
arr_y = np.array([np.sin(x) for x in arr_x])

plt.ylabel("Y axis")
plt.xlabel("X axis")

plt.axis('auto')
plt.axis([0,10,-3,3])
plt.plot(arr_x,arr_y,'b--',arr_x,[np.cos(x) for x in arr_x],'r--',arr_x,[np.tan(x) for x in arr_x], 'y--')
# plt.plot(arr_x, [x**2 for x in arr_x], 'r--', arr_x, [x**3 for x in arr_x], 'y--')
# how can i insert a math function within?

plt.show()