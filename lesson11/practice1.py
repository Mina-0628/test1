"""
practice1.py
使用 Playwright 自動化測試維基百科搜尋功能
 - 透過 placeholder 屬性定位搜尋框
 - 搜尋「臺灣」並擷取文章標題與摘要
"""

from playwright.sync_api import sync_playwright, Playwright, Browser, Page


def crawl(p: Playwright) -> None:
    """
    主要爬蟲函式：執行維基百科自動化搜尋流程
    Args:
        p: Playwright 實例，由 sync_playwright() 產生
    """

    # 1. 啟動 Chromium 瀏覽器（headless=True 表示不顯示瀏覽器視窗）
    browser: Browser = p.chromium.launch(headless=True)
    # 建立一個新的瀏覽器頁面（分頁）
    page: Page = browser.new_page()

    # 2. 前往維基百科中文首頁
    page.goto("https://zh.wikipedia.org")

    # 3. 使用 placeholder（提示文字）定位搜尋框，填入「臺灣」
    #    .first 確保只取得第一個符合的元素
    page.get_by_placeholder("搜尋維基百科").first.fill("臺灣")

    # 4. 截圖保存（用於除錯或紀錄測試過程）
    page.screenshot(path="screenshot.png")

    # 5. 模擬按下 Enter 鍵送出搜尋
    page.keyboard.press("Enter")

    # 6. 等待網路完全空閒（所有請求完成），確保頁面載入完畢
    page.wait_for_load_state("networkidle")

    # 7. 抓取文章大標題（#firstHeading 為維基百科文章標題的 CSS ID）
    first_heading: str = page.locator("#firstHeading").inner_text()
    print(f"搜尋主題: {first_heading}")

    # 8. 抓取第一段摘要文字（#mw-content-text 下的第一個 <p> 標籤）
    #    使用 [:100] 截斷前 100 字元避免輸出過長
    content: str = page.locator("#mw-content-text p").first.inner_text()
    print(f"摘要: {content[:100]}")

    # 9. 返回上一頁（回到維基百科首頁）
    page.go_back()

    # 10. 再次等待網路空閒，確保首頁已完全載入
    page.wait_for_load_state("networkidle")

    # 11. 印出首頁標題，確認已成功返回
    print(f"返回首頁: {page.title()}")

    # 12. 釋放資源：關閉頁面與瀏覽器
    page.close()
    browser.close()


# 使用 sync_playwright 啟動 Playwright 服務，並將實例傳入 crawl 函式
with sync_playwright() as p:
    crawl(p)
