import numpy as np

def is_true_positive(act, pre):
# Actual skip that was correctly predicted as skip
    if act == 0 and pre == 0:
        return True
    else:
        return False

def is_true_negative(act, pre):
# Non-Skip that was correctly predicted as Non-Skip
    if act != 0 and pre != 0:
        return True
    else:
        return False

def is_false_positive(act, pre):
# Non-Skip that was incorrectly predicted as Skip
    if act != 0  and pre == 0:
        return True
    else:
        return False

def is_false_negative(act, pre):
# Skip that was incorrectly predicted as Non-Skip
    if act == 0 and pre != 0:
        return True
    else:
        return False

def get_table_of_confussion(A, P):
    TP = 0 # Number of True Positive
    TN = 0 # Number of True Negative
    FP = 0 # Number of False Positive
    FN = 0 # Number of False Negative
    total = len(A)

    for i in range(total):
        act = A[i]
        pre = P[i]
        if is_true_positive(act, pre):
            TP += 1
        elif is_true_negative(act, pre):
            TN += 1
        elif is_false_positive(act, pre):
            FP += 1
        elif is_false_negative(act, pre):
            FN += 1
    table = dict()
    table['TP'] = TP
    table['TN'] = TN
    table['FP'] = FP
    table['FN'] = FN
    return table