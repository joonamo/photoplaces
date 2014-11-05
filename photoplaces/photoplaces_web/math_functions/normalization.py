import numpy as np
from cyclical_math import *

def dist(a,b):
    return abs(a - b)

def mean_absolute_deviation(values, mean, dist_func = dist):
    return np.sum([dist_func(v,mean) for v in values]) / len(values)

def z_score(values, mean, deviation):
    return (values - mean) / deviation

def cyclical_z_score(v, mean, deviation, cycle_length):
    d = v - mean
    if abs(d) <= cyclical_distance(v, mean, cycle_length):
        k = np.sign(d)
    else: 
        k = -np.sign(d)

    return (k * cyclical_distance(v, mean, cycle_length)) / deviation