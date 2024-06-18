def min_refills(distance, tank, stations):
    # 如果車輛在滿油狀態下能直接到達終點，則不需要加油債
    if distance <= tank:
        return 0, []

    current_pos = 0
    refills = []
    stations.append(distance)  # 將終點當作一個加油站

    for i in range(len(stations)):
        if i == 0:
            continue
        if stations[i] - stations[i - 1] > tank:
            return -1, []  # 兩個加油站之間的距離超過油箱容量，無法完成旅程

        if stations[i] - current_pos > tank:
            current_pos = stations[i - 1]
            refills.append(current_pos)

    return len(refills), refills

# 輸入
n = int(input())
stations = list(map(int, input().split()))
distance = int(input())
tank = 50  # 車輛在滿油狀態下能行駛50公里

num_refills, refills = min_refills(distance, tank, stations)

if num_refills == -1:
    print("無法完成旅程")
elif num_refills == 0:
    print(0)
else:
    for refill in refills:
        print(refill)
