import numpy as np

def trap1(f, a, b, n=10000):
    x=a
    h=(b-a)/n
    sm=0
    integral_values = [0]
    
    for i in range (n-1):
        ar = (f(x)+f(x+h))/2*h
        sm = sm+ar
        integral_values.append(sm)
        x += h
    return np.linspace(a, b, n), integral_values


def trap2(f, a, b, n=100):
    x=a
    h=(b-a)/n
    sm=0
    for i in range (n-1):
        ar = (f(x)+f(x+h))/2*h
        sm = sm+ar
        x = x+h
    return sm
