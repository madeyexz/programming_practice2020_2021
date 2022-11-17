import matplotlib.pyplot as plt
import matplotlib.pylab as pylab 
import numpy as np
import sympy as smp

def f(x):
    return np.abs(pylab.sin(x)*x, x*pylab.cos(x))

range_started = 2*pylab.pi
range_ended = -2*pylab.pi
dot = 10000

x = pylab.linspace(range_started, range_ended, dot)

pylab.plot(x, f(x))

pylab.grid()


# Add a title
plt.title('This my Calculus Python Homework')

# Add X and y Label
plt.xlabel('x axis')
plt.ylabel('y axis')

# Add a grid
#plt.grid(alpha=.4,linestyle='--')

# Add a Legend
# plt.legend()

# Show the plot
plt.show()