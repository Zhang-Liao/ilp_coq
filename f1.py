
def cal_f1(tp, fp, fn):
    denomin = 2 * tp + fp + fn
    if denomin == 0:
        f1 = 0
    else:
        f1 = (2 * tp) / denomin
    return round(f1, 7)

print(cal_f1(446, 1153, 319))