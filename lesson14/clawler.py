import asyncio
import os
import json
from pprint import pprint


# ============================================================
# 0. 專案全域變數設定 (Global Configuration)
# ============================================================
CONFIG_FILE = "products_config.json"

async def main():
    print("=" * 80)
    print(f"毛寶企業 (Maobao) 多賣場產品與競品價格每日監控系統 [Playwright Async版]")
    print("=" * 80)

    # 1. 檢查並讀取 JSON 設定檔 (展現組態驅動設計 Configuration-Driven)
    if not os.path.exists(CONFIG_FILE):
        print(f"錯誤: 找不到設定檔 {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data= json.load(f)
        pprint(config_data)

        categories:list[dict] = config_data.get("monitor_products", [])
             #pprint(categories)
        platforms:list[dict] = config_data.get("platforms", [])
        platform_names = [p["name"] for p in platforms]
        #print(platform_names)
        print(f"📦 載入設定完成！監控 {len(categories)} 大品類，跨賣場：{', '.join(platform_names)}...\n")


if __name__ == "__main__":
    #使用 asyncio 啟動 Python Event Loop
    asyncio.run(main())
