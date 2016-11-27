import numpy as np

def get_marks(count=10, lower=0, upper=1):
    if count == 10 and lower == 0 and upper == 1:
        marks = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        return marks

    marks = []
    interval = (upper - lower) / count
    mark = lower
    # while mark < upper:
    for i in range(count):
        marks.append(mark)
        mark += interval
    marks.append(upper)

    return marks

def get_label(val, marks):
    totle = len(marks)
    for i in range(totle - 1):
        lower = marks[i]
        upper = marks[i+1]
        if i == 0:
            if lower < val and val < upper:
                return i
            continue
        if lower <= val and val < upper:
            return i
    return i + 1 # Other class

def is_same_interval(act, pre, marks):
    total = len(marks)

    for i in range(total-1):
        lower = marks[i]
        upper = marks[i+1]
        if i == 0:
            if (lower < act and act < upper) \
                and (lower < pre and pre < upper):
                return True
            continue
        if (lower <= act and act < upper) \
            and (lower <= pre and pre < upper):
            return True
    return False