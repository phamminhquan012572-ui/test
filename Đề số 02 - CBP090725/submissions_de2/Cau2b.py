s = input()
x = int(input())
y = int(input())
vowels = "aeiouAEIOU"
count = sum(1 for c in s[x - 1:y] if c in vowels)
print(count)
