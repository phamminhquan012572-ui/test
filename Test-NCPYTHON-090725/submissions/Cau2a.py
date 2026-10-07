# a)
def set_ops(s1, s2):
    return (s1 | s2, s1 & s2, s1 - s2)
print(set_ops({1,2,3,4}, {3,4,5,6}))
