# Lesson 11 - 程式碼審查 (Code Review)

> 審查日期：2026-07-22  
> 審查檔案：`form_demo.html`、`practice1.py`、`practice2.py`

---

## 1. form_demo.html

### 優點
- 響應式設計完善，使用 `max-width` + `margin: auto` 實現置中佈局
- 表單欄位皆有 `required` 屬性，具備基本前端驗證
- CSS 使用 `box-sizing: border-box` 避免 padding 撐大元素
- 成功訊息區塊預設 `display: none`，僅在提交後顯示，UX 合理

### 建議改進

| # | 問題 | 嚴重度 | 建議 |
|---|------|--------|------|
| 1 | **無表單資料驗證邏輯** | 中 | `e.preventDefault()` 後直接隱藏表單，未實際處理資料。建議加入 `FormData` 取值並顯示或送出到後端 |
| 2 | **無欄位驗證回饋** | 低 | 雖然有 `required` 屬性，但無自訂錯誤訊息。可使用 `setCustomValidity()` 提供中文錯誤提示 |
| 3 | **無載入動畫/禁用按鈕** | 低 | 提交時按鈕未禁用，使用者可能重複點擊。建議加入 `disabled` 狀態與 loading 動畫 |
| 4 | **`setTimeout` 用途不明** | 低 | 100ms 的 `setTimeout` 僅用於更新 `document.title`，在實際專案中可改用更明確的觸發時機 |
| 5 | **CSS 可抽取為外部樣式表** | 低 | 若專案擴大，建議將 `<style>` 拆分為獨立 `.css` 檔案 |
| 6 | **無 `<footer>` 或版權資訊** | 低 | 頁面缺乏版權聲明或聯絡資訊 |

### 建議改進範例（表單資料驗證）

```javascript
document.getElementById('registrationForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // 使用 FormData 取得表單資料
    const formData = new FormData(this);
    const name = formData.get('name');
    const email = formData.get('email');
    const country = formData.get('country');
    const subscribe = formData.has('subscribe');

    console.log({ name, email, country, subscribe });

    // TODO: 將資料送到後端 API
    // fetch('/api/register', { method: 'POST', body: formData });

    // 顯示成功訊息
    this.style.display = 'none';
    document.getElementById('successMessage').style.display = 'block';
    document.title = '提交成功';
});
```

---

## 2. practice1.py

### 優點
- 型別標註完整（`Playwright`、`Browser`、`Page`、`str`）
- 註解清晰，步驟編號明確
- 使用 `networkidle` 等待策略確保頁面載入完畢
- 正確關閉頁面與瀏覽器釋放資源

### 建議改進

| # | 問題 | 嚴重度 | 建議 |
|---|------|--------|------|
| 1 | **截圖檔名固定為 `screenshot.png`** | 中 | 每次執行會覆蓋舊檔。建議使用時間戳或動態檔名（如 `screenshot_{timestamp}.png`） |
| 2 | **無例外處理 (try/except)** | 高 | 若網站回應異常或元素不存在，程式會直接崩潰。應加入 `try/except` 區塊 |
| 3 | **無頁面逾時設定** | 中 | `wait_for_load_state("networkidle")` 無逾時上限，若伺服器無回應會永久卡住。建議加入 `timeout` 參數 |
| 4 | **摘要截斷硬編碼 `[:100]`** | 低 | 100 字元可能切斷句子。建議使用 `textwrap.shortwrap()` 或改為按句子截斷 |
| 5 | **缺少 `if __name__ == "__main__"` 護欄** | 低 | 直接執行 `with sync_playwright()` 無法作為模組匯入。建議加入主程式護欄 |
| 6 | **`page.close()` 與 `browser.close()` 無在 `finally` 區塊** | 中 | 若中途發生例外，資源不會被釋放。建議使用 `try/finally` 確保清理 |

### 建議改進範例（加入例外處理與資源管理）

```python
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, Browser, Page


def crawl(p: Playwright) -> None:
    browser: Browser | None = None
    page: Page | None = None

    try:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://zh.wikipedia.org", timeout=30000)
        page.get_by_placeholder("搜尋維基百科").first.fill("臺灣")

        # 使用時間戳避免截圖覆蓋
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshot_{timestamp}.png")

        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle", timeout=30000)

        first_heading = page.locator("#firstHeading").inner_text()
        print(f"搜尋主題: {first_heading}")

        content = page.locator("#mw-content-text p").first.inner_text()
        print(f"摘要: {content[:100]}")

        page.go_back()
        page.wait_for_load_state("networkidle", timeout=30000)
        print(f"返回首頁: {page.title()}")

    except Exception as e:
        print(f"發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if page:
            page.close()
        if browser:
            browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        crawl(p)
```

---

## 3. practice2.py

### 優點
- 與 practice1.py 結構一致，便於比較兩種定位方式的差異
- 使用 `#searchInput` ID 選擇器，定位更精確穩定
- 註解清楚標註與 practice1 的差異點

### 建議改進

| # | 問題 | 嚴重度 | 建議 |
|---|------|--------|------|
| 1 | **與 practice1.py 重複度極高** | 中 | 兩個檔案 90% 以上程式碼相同。建議抽取共用函式（如 `search_wiki(p, query, method)`），以 `method` 參數區分定位方式 |
| 2 | **無例外處理** | 高 | 同 practice1.py，缺少 try/except |
| 3 | **截圖檔名固定** | 中 | 同 practice1.py，每次執行覆蓋舊檔 |
| 4 | **無頁面逾時設定** | 中 | 同 practice1.py |
| 5 | **print 格式不一致** | 低 | 第 26 行 `搜尋主題:` 後缺少空格，與第 37 行一致但與 practice1.py 不同。建議統一格式 |
| 6 | **缺少 `if __name__ == "__main__"` 護欄** | 低 | 同 practice1.py |

### 建議重構：抽取共用函式

```python
"""
wiki_search.py
維基百科自動化搜尋工具 - 抽取共用邏輯
"""

import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, Browser, Page


def search_wiki(
    p: Playwright,
    query: str = "臺灣",
    method: str = "id",  # "id" 或 "placeholder"
) -> None:
    """執行維基百科搜尋並回傳結果"""
    browser: Browser | None = None
    page: Page | None = None

    try:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://zh.wikipedia.org", timeout=30000)

        # 根據 method 選擇不同的定位方式
        if method == "id":
            page.locator("#searchInput").fill(query)
        else:
            page.get_by_placeholder("搜尋維基百科").first.fill(query)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshot_{timestamp}.png")

        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle", timeout=30000)

        heading = page.locator("#firstHeading").inner_text()
        content = page.locator("#mw-content-text p").first.inner_text()

        print(f"搜尋主題: {heading}")
        print(f"摘要: {content[:100]}")

        page.go_back()
        page.wait_for_load_state("networkidle", timeout=30000)
        print(f"返回首頁: {page.title()}")

    except Exception as e:
        print(f"發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if page:
            page.close()
        if browser:
            browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        # 切換 method="placeholder" 可改用 placeholder 定位
        search_wiki(p, method="id")
```

---

## 整體建議摘要

### 高優先度
- **加入例外處理**：所有 Playwright 腳本都應有 `try/except/finally` 保護，避免資源洩漏
- **加入逾時設定**：`goto()` 和 `wait_for_load_state()` 應設定合理 `timeout`

### 中優先度
- **避免程式碼重複**：practice1 與 practice2 應抽取共用函式
- **截圖檔名動態化**：避免每次執行覆蓋舊檔

### 低優先度
- **加入 `if __name__ == "__main__"` 護欄**
- **統一 print 格式**（空格、標點）
- **HTML 表單加入實際資料處理邏輯**
