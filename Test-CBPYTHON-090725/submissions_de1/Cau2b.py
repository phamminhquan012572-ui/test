
s = input()
x = int(input())
y = int(input())
count = 0
for c in s[x-1:y]:
    if c.isdigit():
        count += 1
print(count)
