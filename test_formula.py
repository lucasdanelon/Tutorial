"""
Created on Mon Sep  7 16:54:55 2020

@author: rodrigo
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,201,1)   # start,stop,step

def focal_loss(p,maximum,lam=0.5):
    base = -(1-maximum)**lam*np.log(maximum)
    if p==0:
        return (base+(1-2*maximum)**lam*np.log(2*maximum))/2
    coef = base+(1-p)**lam*np.log(p)
    return coef

def apply_formula(x,lam=0.5):
    maximum = np.max(x)
    x=x/maximum
    result = np.zeros((len(x)))
    for index,k in enumerate(x):
        result[index] = focal_loss(k,0.5/maximum,lam)
    return result

hf = plt.figure()
ha = hf.add_subplot(111)

for lam in np.arange(0,3.1,0.5):
    result = apply_formula(x,lam)
    ha.plot(x, result, label=str(lam))

ha.legend()
plt.show()
