#a)
def count_freq(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1
    return d
print(count_freq("hello world"))