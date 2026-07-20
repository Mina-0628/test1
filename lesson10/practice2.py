import time
import asyncio

async def download_file_async(file_name):#async若遇到等待先給別做
  print(f"開始下載 {file_name}...")
  await asyncio.sleep(2) #整個程式總共耗時兩秒.await (關鍵字)：意思是「在這裡等待，但別人可以先插隊」
  print(f"✅ {file_name} 下載完成")
  return f"{file_name}_data"

async def main_async():
  start = time.time()

  results = await asyncio.gather(
    download_file_async("檔案A.pdf"),
    download_file_async("檔案B.pdf"),
    download_file_async("檔案C.pdf"),
  )

  end = time.time()
  print(f"\n總耗時: {end - start:.2f} 秒")

if __name__ == "__main__":
  asyncio.run(main_async())  #這邊建立event loop 一個執行的全組