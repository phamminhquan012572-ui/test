x = int(input())
y = int(input())
tong_chan = sum(i for i in range(x, y+1) if i % 2 == 0)
print(tong_chan)
