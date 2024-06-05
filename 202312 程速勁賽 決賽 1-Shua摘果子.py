def maxTime(Tree, Tree_Apple):

    total_time = 0
    # 當一棵樹的蘋果大於5顆，那Shua會請工人摘蘋果，所以Shua的工時不計入
    for apples in Tree_Apple:
        apples = int(apples)
        if apples > 5:
            continue
        else:
            total_time += apples * 5
    if Tree > 1:
        total_time += (Tree - 1) * 10
    return total_time

# 輸入
Tree = int(input())
Tree_Apple = input().split()

# 輸出
print(maxTime(Tree, Tree_Apple))