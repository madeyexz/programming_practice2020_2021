# 这个题你会不：30个海盗困在一个荒岛上，但是现有粮食只能维持15个人活着
# 海盗们决定用这样一种方式扔下15个人喂海里的鲨鱼
# 他们按1号到30号进行编号并逆时针围成一个圈
# 从1号开始数数，从1数到9，数到9的人被扔下去
# 下一个人继续从1开始数，以此类推每次数到9的人都被扔下去（即9号 18号 27号 6号……）
# 直到剩下15个人，请输出：最后留在岛上的人的编号

ppl = [i for i in range(1, 31)]

i = 0
while len(ppl) > 15:
    i += 9
    if i > len(ppl):
        i = i % len(ppl)
    del ppl[i-1]
    i -= 1

print(ppl)
    