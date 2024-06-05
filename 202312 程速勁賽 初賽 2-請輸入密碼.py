def verify_password(input_str, real_password):
    password = ""
    for char in input_str:
        if char == "#":
            if len(password) > 0:
                password = password[:-1]
        else:
            password += char
    return password == real_password


k = input()
p = input()

if 1 <= len(k) <= 500 and 1 <= len(p) <= 100:
    # 執行其他程式邏輯

    result = verify_password(k, p)

    if result:
        print("Successful")
    else:
        print("Error")
else:
    if not (1 <= len(k) <= 500):
        print("輸入的字串長度不在範圍內")
    if not (1 <= len(p) <= 100):
        print("密碼長度不在範圍內")

