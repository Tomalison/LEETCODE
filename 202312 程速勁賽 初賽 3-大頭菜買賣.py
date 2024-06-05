def maxProfit(prices, F):
    N = len(prices)
    if N == 0:
        print("Error: 價格序列不能為空")
        return 0

    try:
        # 初始化第一天的狀態
        hold = -prices[0]
        notHold = 0

        for i in range(1, N):
            newHold = max(hold, notHold - prices[i])
            newNotHold = max(notHold, hold + prices[i])

            # 更新狀態
            hold = newHold
            notHold = newNotHold

        # 最後一天不持有的最大收益
        profit = notHold
        print(profit)
        return profit
    except ValueError:
        print("Error: 價格序列必須全部為數字")
        return 0


# 從使用者輸入價格序列和天數F
F = int(input())
prices = input().split()

try:
    prices = [int(price) for price in prices]
    maxProfit(prices, F)
except ValueError:
    print("Error: 價格序列必須全部為整數")