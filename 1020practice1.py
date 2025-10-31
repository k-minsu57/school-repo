import numpy as np

from Trap_function import trap2

stdnormdens = lambda z: 1/np.sqrt(2*np.pi)*np.exp(-1/2*z**2)
a = -1.3
b = -0.3
P = trap2(stdnormdens, a, b)
print('probability={0:6.1f}%'.format(P*100))