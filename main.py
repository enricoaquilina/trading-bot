import numpy as np

dataset = [1, 5, 7, 2, 6, 7, 8, 2, 6, 13]


def movingaverage(values, window):
    weights = np.repeat(1, window) / window
    smas = np.convolve(values, weights,'valid')
    return smas

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1, 0, num=window))
    weights /= weights.sum()

    t = np.convolve([1,1,5,5],[3,4,2])
    a = np.convolve(values, weights,'valid')#[:len(values)]
    a[:window]=a[window]
    return a

# print(movingaverage(dataset,3))
print(ExpMovingAverage(dataset, 3))
