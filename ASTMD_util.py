import numpy as np


def avg(parameter):
    lengths = [len(vector) for vector in parameter]
    scope = [0]
    average = []
    index = list(range(len(parameter)))

    while len(lengths) > 0:
        scope.append(min(lengths))
        for i in range(scope[-2], scope[-1]):
            average.append(sum([column[i] for column in [parameter[ele] for ele in index]]) / len(lengths))
        index.pop(lengths.index(scope[-1]))
        lengths.pop(lengths.index(scope[-1]))

    return average


def find_index(vector, value):
    errors = [abs(number-value) for number in vector]
    return errors.index(min(errors))
