# b)
def get_high_scores(d, min_score):
    return [k for k, v in d.items() if v >= min_score]
score = {"An": 8, "Binh": 6, "Cuong": 9, "Dung": 5, "Hoa": 8}
print(get_high_scores(score, 8))