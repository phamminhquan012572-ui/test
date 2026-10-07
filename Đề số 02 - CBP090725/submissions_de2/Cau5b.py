def find_max_price(d):
    return max(d, key=d.get)

prices = {"apple": 20, "banana": 10, "orange": 15}
print(find_max_price(prices))
