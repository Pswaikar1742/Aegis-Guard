import numpy as np


def leading_digit_distribution(numbers):
    digits = [int(str(abs(int(x)))[0]) for x in numbers if x != 0]
    counts = np.bincount(digits, minlength=10)[1:]
    return counts / counts.sum()
