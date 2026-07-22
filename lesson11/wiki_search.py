"""
wiki_search.py
維基百科自動化搜尋工具（合併 practice1 與 practice2）
 - 支援兩種定位方式：placeholder / ID 選擇器
 - 參數化設計，便於擴展與維護
"""

import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, Browser, Page


def search_wiki(
    p: Playwright,
    query: str = "臺灣",
    method: str = "id",        # "id" 或 "placeholder"
    headless: bool = True,
    timeout: int = 30000,
) -> None:
    """
    執行維基百科自動化搜尋
    Args:
        p:         Playwright 實例
        query:     搜尋關鍵字，預設「臺灣」
        method:    定位方式，"id" 使用 #searchInput，"placeholder" 使用提示文字
        headless:  是否隱藏瀏覽器視窗
        timeout:   頁面載入逾時毫秒數
    """
    browser: Browser | None = None
    page: Page | None = None

    try:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # 前往維基百科中文首頁
        page.goto("https://zh.wikipedia.org", timeout=timeout)

        # 根據 method 選擇不同的元素定位方式
        if method == "id":
            # 使用 CSS ID 選擇器定位（較精確）
            page.locator("#searchInput").fill(query)
        else:
            # 使用 placeholder 提示文字定位（較直觀）
            page.get_by_placeholder("搜索维基百科").first.fill(query)

        # 截圖保存（使用時間戳避免覆蓋）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshot_{timestamp}.png")

        # 按下 Enter 送出搜尋
        page.keyboard.press("Enter")

        # 等待頁面載入完畢（使用 domcontentloaded 避免 networkidle 超時）
        page.wait_for_load_state("domcontentloaded", timeout=timeout)
        page.locator("#firstHeading").wait_for(timeout=timeout)

        # 抓取文章標題與摘要
        first_heading: str = page.locator("#firstHeading").inner_text()
        content: str = page.locator("#mw-content-text p").first.inner_text()

        print(f"搜尋主題: {first_heading}")
        print(f"摘要: {content[:100]}")

        # 返回上一頁並等待載入
        page.go_back()
        page.wait_for_load_state("domcontentloaded", timeout=timeout)
        print(f"返回首頁: {page.title()}")

    except Exception as e:
        print(f"[錯誤] {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        # 確保資源一定被釋放
        if page:
            page.close()
        if browser:
            browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        search_wiki(p, query="臺灣", method="id")
