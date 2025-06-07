import math
import numpy as np

def my_max(data):
    maximum = data[0]
    for x in data:
        if x > maximum:
            maximum = x
    return maximum

def my_min(data):
    minimum = data[0]
    for x in data:
        if x < minimum:
            minimum = x
    return minimum

def my_mean(data):
    total = 0
    for x in data:
        total += x
    return total / len(data)

def my_std(data, mean):
    variance = 0
    for x in data:
        variance += (x - mean) ** 2
    return math.sqrt(variance / len(data))

def my_sort(data):
    sorted_data = data[:]
    for i in range(len(sorted_data)):
        for j in range(i + 1, len(sorted_data)):
            if sorted_data[j] < sorted_data[i]:
                sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
    return sorted_data

def get_percentile(p, data_sorted, n):
    k = (n - 1) * p
    f = int(k)
    c = f + 1 if f + 1 < n else f
    return data_sorted[f] + (data_sorted[c] - data_sorted[f]) * (k - f)

def my_quartiles(data):
    data_sorted = my_sort(data)
    n = len(data_sorted)
    q1 = get_percentile(0.25, data_sorted, n)
    q2 = get_percentile(0.5, data_sorted, n)
    q3 = get_percentile(0.75, data_sorted, n)
    return q1, q2, q3

def pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("Inputs x and y must have the same length.")

    n = len(x)
    mean_x = my_mean(x)
    mean_y = my_mean(y)
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n))

    if denominator_x == 0 or denominator_y == 0:
        return 0

    return numerator / math.sqrt(denominator_x * denominator_y)

#transforme une valeur en une probabilité entre 0 et 1
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
