import numpy as np

def cyclical_distance(a, b, cycle_length):
    linear_dist = abs(a - b)
    return min(linear_dist, cycle_length - linear_dist)

def cycle_v_to_rad(v, cycle_length):
    return (v % cycle_length) * np.pi * 2 / cycle_length

def cycle_v_to_quaternion(v, cycle_length):
    v = cycle_v_to_rad(v, cycle_length)
    return np.array([np.cos(v), np.sin(v)])

def quaternion_to_cycle_v(q, cycle_length):
    v = np.arctan2(q[1], q[0]) * cycle_length / np.pi / 2
    if v < 0:
        return v + cycle_length
    else:
        return v

def cycle_avg(values, cycle_length, **kwargs):
    weights = kwargs.get("weights")
    if weights is None:
        weights = np.ones(len(values))
    weights = np.array([weights, weights]).transpose()
    quaternions = np.array([cycle_v_to_quaternion(v, cycle_length) for v in values])
    quaternions = quaternions * weights
    s = np.sum(quaternions, axis=0)
    return quaternion_to_cycle_v(s / np.linalg.norm(s), cycle_length)

def month_wrap(v):
    while v < 1:
        v += 12
    while v > 12:
        v -= 12
    return v