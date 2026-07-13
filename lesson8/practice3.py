import random


def playgame():
    # 產生 1~100 的隨機整數作為答案
    target = random.randint(1, 100)
    # 設定搜尋範圍的上下界
    low, high = 1, 100
    attempts = 0

    # 遊戲標題與說明
    print("猜數字遊戲（範圍縮小版）")
    print(f"請猜一個介於 {low} ~ {high} 之間的數字\n")
    #不知道猜幾次用while真實True迴圈.

    while True:
        # 取得玩家輸入，處理非數字的例外狀況
        try:
            guess = int(input(f"請輸入你的猜測（{low} ~ {high}）："))
        except ValueError:
            print("請輸入有效數字\n")
            continue

        # 檢查輸入是否超出目前的有效範圍
        if guess < low or guess > high: #猜的guess小於low大於high:
            print(f"超出範圍，請輸入 {low} ~ {high} 之間的數字\n")
            continue #繼續


        # 猜測次數加一
        attempts += 1

        # 判斷猜測結果
        if guess == target: #guess為輸入值 target為目標值
            # 猜中，顯示答案與總次數，結束迴圈
            print(f"🎉 恭喜你猜中了！答案就是 {target}")
            print(f"你總共猜了 {attempts} 次")
            break #結束程式
        elif guess < target:
            # 猜太小，將下界提高到 guess+1 以縮小範圍
            low = guess + 1 #新的輸入值已經猜的數字+1為新的low
            print(f"再大一點！範圍縮小為 {low} ~ {high}\n")
        else:
            # 猜太大，將上界降低到 guess-1 以縮小範圍
            high = guess - 1  #新的輸入值已經猜的數字-1為新的high
            print(f"再小一點！範圍縮小為 {low} ~ {high}\n")

while True:
    playgame()
    isplay=input("您還要繼續嗎?(y.n)")
    if isplay == "n":
        break
