"""함수 그래프 그리기
sin(x) 함수를 지정한 범위 [0, 3pi]의 어쩌구...
"""

import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return np.sin(x)

if __name__ == "__main__":
    x = np.linspace(0, np.pi * 3)
    plt.plot(x, func(x))
    plt.grid(True)
    plt.show()