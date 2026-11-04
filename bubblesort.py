num = [2,5,9,1,9]
n = len(num)
for i in range(n):
    for j in range(n-1):
        if num[j] > num[j + 1]:
            num[j], num[j + 1] = num[j + 1],num[j]
print(num)    