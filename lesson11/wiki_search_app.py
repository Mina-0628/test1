"""
wiki_search_app.py
維基百科自動化搜尋工具 - Web GUI 版本
使用 Python 內建 http.server，無需安裝额外套件
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime


def run_search(query: str, method: str, headless: bool, timeout: int) -> dict:
    """
    執行搜尋並回傳結果
    Returns:
        dict: {"success": bool, "heading": str, "summary": str, "error": str}
    """
    try:
        from playwright.sync_api import sync_playwright

        # 擷取輸出結果
        results = {"success": False, "heading": "", "summary": "", "error": ""}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()

            page.goto("https://zh.wikipedia.org", timeout=timeout)

            if method == "id":
                page.locator("#searchInput").fill(query)
            else:
                page.get_by_placeholder("搜索维基百科").first.fill(query)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(os.path.dirname(__file__), f"screenshot_{timestamp}.png")
            page.screenshot(path=screenshot_path)

            page.keyboard.press("Enter")
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
            page.locator("#firstHeading").wait_for(timeout=timeout)

            results["heading"] = page.locator("#firstHeading").inner_text()
            content = page.locator("#mw-content-text p").first.inner_text()
            results["summary"] = content[:200]
            results["success"] = True

            page.close()
            browser.close()

        return results

    except Exception as e:
        return {"success": False, "heading": "", "summary": "", "error": str(e)}


class WikiSearchHandler(BaseHTTPRequestHandler):
    """HTTP 請求處理器"""

    def do_GET(self):
        """處理 GET 請求 - 回傳 HTML 頁面"""
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
            with open(html_path, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        """處理 POST 請求 - 執行搜尋"""
        if self.path == "/api/search":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)

            query = params.get("query", ["臺灣"])[0]
            method = params.get("method", ["id"])[0]
            headless = params.get("headless", ["true"])[0] == "true"
            timeout = int(params.get("timeout", ["30000"])[0])

            print(f"[搜尋] query={query}, method={method}, headless={headless}")

            results = run_search(query, method, headless, timeout)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(results, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        """自訂日誌格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    host = "127.0.0.1"
    port = 5500

    server = HTTPServer((host, port), WikiSearchHandler)
    print("=" * 50)
    print("  維基百科搜尋工具 - Web GUI")
    print(f"  http://{host}:{port}")
    print("  按 Ctrl+C 停止伺服器")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")
        server.server_close()


if __name__ == "__main__":
    main()
