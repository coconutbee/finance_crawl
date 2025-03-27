import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from repair import repair_csv_files  # 假設這個模組能修正亂碼 CSV

def crawl_twse_data():
    # 1. 設定主要下載路徑 (全部先下載到這裡)
    download_dir = os.path.abspath("twse_data")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # 2. 配置 Chrome 下載選項
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,  # 自動下載路徑
        "download.prompt_for_download": False,       # 不顯示下載詢問對話框
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # 如果不需要顯示瀏覽器，可以加上 headless 模式
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        url = "https://www.twse.com.tw/zh/trading/historical/fmtqik.html"
        driver.get(url)
        time.sleep(3)  # 等待頁面初始載入

        # 年度、月份下拉選單
        year_select_elem = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[name="yy"]'))
        )
        month_select_elem = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[name="mm"]'))
        )

        # 迭代民國 79 ~ 113 年，1 ~ 12 月
        for min_guo_year in range(79, 114):
            # year_select
            real_year = min_guo_year + 1911  # 下拉選單中的 value
            year_select = Select(year_select_elem)
            year_value = str(real_year)
            year_select.select_by_value(year_value)
            time.sleep(1)

            # 建立該民國年的資料夾
            year_folder = os.path.join(download_dir, f"民國{str(min_guo_year)}年")
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            for month in range(1, 13):
                # 選擇月份
                month_select = Select(month_select_elem)
                month_value = str(month)
                month_select.select_by_value(month_value)
                time.sleep(1)

                # 點擊 CSV 下載按鈕
                csv_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.csv'))
                )
                csv_button.click()
                print(f"已點擊下載：民國{min_guo_year}年{month}月")

                # 等待下載完成
                time.sleep(3)

                # 取得剛剛下載的檔案（fmthtq.csv 或 fmthtq(1).csv 等）
                downloaded_files = glob.glob(os.path.join(download_dir, "FMTQIK*.csv"))
                if not downloaded_files:
                    print("找不到剛下載的 CSV 檔案，可能下載失敗。")
                    continue

                # 找到最後修改時間最新的那個檔案
                latest_file = max(downloaded_files, key=os.path.getmtime)

                # 搬移到 twse_data/{min_guo_year}/
                # 並將檔名改為 {month}.csv
                new_filename = f"{month}月.csv"
                new_path = os.path.join(year_folder, new_filename)
                os.rename(latest_file, new_path)
                print(f"下載並移動檔案: {new_path}")

    except Exception as e:
        print("發生錯誤：", e)
    finally:
        driver.quit()

    return download_dir

if __name__ == "__main__":
    dir = crawl_twse_data()
    repair_csv_files(dir)  # 將剛下載的 CSV 進行亂碼修復
