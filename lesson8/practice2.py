import random

# 產生 1~100 的隨機整數作為答案
target = random.randint(1, 100)
# 設定搜尋範圍的上下界
low, high = 1, 100
# 記錄玩家猜測次數
attempts = 0

# 遊戲標題與說明
print("猜數字遊戲（範圍縮小版）")
print(f"請猜一個介於 {low} ~ {high} 之間的數字\n")

# 進入遊戲主迴圈，直到猜中為止
while True:
    # 取得玩家輸入，處理非數字的例外狀況
    try:
        guess = int(input(f"請輸入你的猜測（{low} ~ {high}）："))
    except ValueError:
        print("請輸入有效數字\n")
        continue

    # 檢查輸入是否超出目前的有效範圍
    if guess < low or guess > high:
        print(f"超出範圍，請輸入 {low} ~ {high} 之間的數字\n")
        continue

    # 猜測次數加一
    attempts += 1

    # 判斷猜測結果
    if guess == target:
        # 猜中，顯示答案與總次數，結束迴圈
        print(f"🎉 恭喜你猜中了！答案就是 {target}")
        print(f"你總共猜了 {attempts} 次")
        break
    elif guess < target:
        # 猜太小，將下界提高到 guess+1 以縮小範圍
        low = guess + 1
        print(f"太小了！範圍縮小為 {low} ~ {high}\n")
    else:
        # 猜太大，將上界降低到 guess-1 以縮小範圍
        high = guess - 1
        print(f"太大了！範圍縮小為 {low} ~ {high}\n")
