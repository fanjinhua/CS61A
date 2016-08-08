ls = [11, 22, 33, 44]

                # 4
for i in range(len(ls)):
    if i == (len(ls) - 1):
        i = -1
    print(ls[i+1])