def number_guest(H, n):
    count = 0
    lower = 1
    upper = H

    while True:
        count += 1
        guess = (lower + upper)// 2

        if guess == n:
            return count
        elif guess < n:
            lower = guess + 1
        else:
            upper = guess - 1


a = int(input())
b = int(input())

tries = number_guest(a, b)
print(tries)