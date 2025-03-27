import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def download_csv_files(name: str, url: str, result: str) -> str:
    # 1. 用 Selenium 進入目標查詢頁面並完成查詢
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    
    # 進入 MOPS 查詢頁面（此 URL 需根據實際情況調整）
    driver.get(url)
    
    # 等待網頁及 AJAX 載入（根據網頁狀況調整等待時間）
    time.sleep(5)
    
    # 2. 取得當前完整 HTML，並用 BeautifulSoup 解析
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    
    # 3. 抓取所有隱藏欄位 (input type="hidden") 中，name 為 "filename" 的值
    filename_inputs = soup.find_all("input", {"name": "filename"})
    filenames = [inp.get("value") for inp in filename_inputs if inp.get("value")]
    print("找到的 filename 清單：", filenames)
    
    # 4. 取得 Selenium 中的 Cookie，供 requests 使用
    selenium_cookies = driver.get_cookies()
    driver.quit()
    
    # 5. 建立 requests Session，並把 Selenium Cookie 注入
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path")
        )
    
    # 6. 設定下載 CSV 所需的 POST 參數與目標 URL
    # 依據表單，下載 URL 應該為 "/server-java/t105sb02"，完整 URL 請依照實際情況調整
    download_url = "https://mopsov.twse.com.tw/server-java/t105sb02"
    # web_list_url = ["https://mopsov.twse.com.tw/mops/#/web/t163sb05", "https://mopsov.twse.com.tw/mops/#/web/t163sb04"] #"https://mopsov.twse.com.tw/mops/web/ajax_t163sb20", 
    # for web_url in web_list_url:
    if result == "t163sb05":
        download_folder = "Balance_Sheet"
    elif result == "t163sb04":
        download_folder = "Income_Statement"
    elif result == "t163sb20":
        download_folder = "Cash_Flow"
    elif result == "t163sb02":
        download_folder = "Financial_Analysis"
    else:
        download_folder = "Others"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Referer": "https://mopsov.twse.com.tw/mops/#/web/t163sb05"
    }
    
    # 建立儲存資料夾
    drop_folder = f"{download_folder}/{name}"
    if not os.path.exists(drop_folder):
        os.makedirs(drop_folder)
    
    # 7. 對每個 filename 發送 POST 請求下載 CSV 檔案
    for fn in filenames:
        payload = {
            "firstin": "true",
            "step": "10",
            "filename": fn,
            "saveCSV": "Y"
        }
        # print("正在下載 CSV 檔案:", fn)
        response = session.post(download_url, data=payload, headers=headers)
        if response.status_code == 200:
            file_path = os.path.join(drop_folder, fn)
            with open(file_path, "wb") as f:
                f.write(response.content)
            # print("下載成功，存為：", file_path)
        else:
            print("下載失敗，狀態碼：", response.status_code, "檔案：", fn)
    
    return download_folder

if __name__ == "__main__":
    name =  "113年第一季"
    url = "https://mopsov.twse.com.tw/mops/web/ajax_t163sb20?parameters=0eb65210d5bdc34ea16e295ccdbad1090f047490e2301f1ba68b34164525fa5065faf210140df5242aa5cd204feb01454cfcee0014abbd5298e3b47bc21f4be9b4afa81caedbae6ad2b2cc9fb052c058ac227a1154318f40f7d39b245c666992af8fd30850b595f9984f08bcb26a48272a317cbd30cfd6183c2450b532cf3c86"
    result = "t163sb20"
    download_csv_files(name, url, result)