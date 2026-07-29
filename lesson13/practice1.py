import time
from playwright.sync_api import Browser, Page, Playwright, sync_playwright


def search_and_print_thsrc_trains(p: Playwright):
    # 1. 啟動瀏覽器並隱藏自動化痕跡
    browser: Browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
    )
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    )
    page: Page = context.new_page()

    print("1. 正在前往台灣高鐵官網...")
    page.goto("https://www.thsrc.com.tw/")
    page.wait_for_timeout(1000)

    # 點擊 Cookie 同意按鈕
    try:
        agree_btn = page.get_by_role("button", name="我同意", exact=True)
        if agree_btn.is_visible(timeout=3000):
            agree_btn.click()
            print("✓ 已點擊「我同意」按鈕")
    except Exception:
        print("未偵測到「我同意」彈窗，繼續執行...")

    print("2. 設定行程資訊（單程：台北 ➔ 台中）...")

    # 選擇地點（您原本寫法無誤）
    page.locator("#select_location01").select_option(value="TaiPei")
    page.locator("#select_location02").select_option(value="TaiZhong")

    # 設定日期（您原本的打字邏輯）
    depart_date = page.locator("#Departdate01")
    depart_date.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    depart_date.type("2026/07/29", delay=50)
    page.keyboard.press("Enter")

    # 設定時間（您原本的打字邏輯 - 還原 input 填寫）
    out_time = page.locator("#outWardTime")
    out_time.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    out_time.type("19:00", delay=50)
    page.keyboard.press("Enter")

    page.wait_for_timeout(1000)

    print("3. 點擊查詢按鈕...")
    # 點擊查詢 (不使用嚴格的 expect_navigation，避免 URL 關鍵字比對失敗)
    page.locator("#start-search").click()

    print("4. 已點擊查詢，等待車次列表載入...")

    try:
        # ★【關鍵修正處】原本的 .tr-number 不存在，改用 DOM 中真實存在的 HTML 元素
        # #timeTableTrain_S 是時刻表容器，a.tr-row 是每一列的班次
        train_locator = page.locator("#timeTableTrain_S a.tr-row")
        train_locator.first.wait_for(state="visible", timeout=15000)
    except Exception as e:
        print(f"⚠️ 載入逾時：{e}")
        page.screenshot(path="error_page.png")
        browser.close()
        return

    print("\n" + "=" * 45)
    print(" 搜尋到的車次（班次）列表：")
    print("=" * 45)

    # 抓取所有車次容器並印出結果
    rows = train_locator.all()
    seen_trains = set()

    for row in rows:
        # 抓取車次號碼（位於 .tr-td.train 裡面）
        train_num_el = row.locator(".tr-td.train")
        train_num = train_num_el.inner_text().strip() if train_num_el.count() > 0 else ""

        # 抓取時間資訊
        times = row.locator(".font-16r").all_inner_texts()
        dept_time = times[0].strip() if len(times) > 0 else ""
        arr_time = times[1].strip() if len(times) > 1 else ""

        if train_num and train_num not in seen_trains:
            seen_trains.add(train_num)
            print(f"車次：{train_num:<6} | 出發時間：{dept_time} ➔ 抵達時間：{arr_time}")

    print("=" * 45)
    print("\n程式執行完成，5 秒後關閉瀏覽器...")
    page.wait_for_timeout(5000)
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        search_and_print_thsrc_trains(p)
