lst = [100, "apple", 3.14, "banana", 200, None]
list_str = [x for x in lst if isinstance(x, str)]
print(list_str)
