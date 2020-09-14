"""
Created on Mon Sep  7 16:54:55 2020

@author: rodrigo
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1,51,1)   # start,stop,step

def score(n_elems, p_elem):
    coef = 1.5**(n_elems - p_elem)/(np.sum(1.5**(np.arange(1, n_elems + 1 ) - 1)))
    return coef

def focal_loss(p,lam=2):
    coef = -(1-p)**lam*np.log(p)
    return coef

def apply_formula(x):
    result = np.zeros((len(x),len(x)))
    for j in x:
        for k in np.arange(1,j+1):
            result[j-1][k-1] = score(j,k)
            
    return result


result = apply_formula(x)

hf = plt.figure()
ha = hf.add_subplot(111, projection='3d')

X, Y = np.meshgrid(x, x)  # `plot_surface` expects `x` and `y` data to be 2D
ha.plot_surface(X, Y, result)

plt.show()