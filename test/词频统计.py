dt = {}
while True:
    try:
        wd = input()
        if wd in dt:  # 如果有元素键为wd
            dt[wd] += 1
        else:
            dt[wd] = 1  # 加入键为wd的元素，其值是1
    except:
        break  # 输入结束后的input()引发异常，调到这里，再跳出循环
result = []
for x in dt.items():
    result.append(x)  # x是个元组，x[0]是单词，x[1]是出现次数
result.sort(key=lambda x: (-x[1], x[0]))
for x in result:
    print(x[1], x[0])
