import numpy as np
__author__ = 'minjoon'

def log_normalize(distribution):
    if len(distribution) == 0:
        return distribution
    log_sum_value = np.log(sum(np.exp(logp) for _, logp in distribution.iteritems()))
    normalized_distribution = {key: value - log_sum_value for key, value in distribution.iteritems()}
    assert is_log_consistent(normalized_distribution)
    return normalized_distribution


def is_log_consistent(distribution, eps=0.01):
    sum_value = sum(np.exp(logp) for _, logp in distribution.iteritems())
    return np.abs(1-sum_value) < eps


def log_add(distribution, key, logp):
    if key in distribution:
        distribution[key] = np.log(np.exp(distribution[key]) + np.exp(logp))
    else:
        distribution[key] = logp