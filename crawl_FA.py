import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from downloader import download_csv_files
from repair import repair_csv_files
from remove_empty import repair_csv

def get_query_links(main_url, years, quarters):
    # 初始化 WebDriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    
    # 開啟查詢主頁
    driver.get(main_url)
    time.sleep(2)  # 等待初步載入
    main_window = driver.current_window_handle

    links = []  # 用來存 (year, quarter, query_result_page URL)

    for year in years:
        for quarter in quarters:
            print(f"處理年度 {year}、季度 {quarter} 的查詢...")
            # 在主頁上進行查詢設定：
            # 1. 選擇「市場所別」=「上市」
            market_select = wait.until(EC.element_to_be_clickable((By.ID, "TYPEK")))
            Select(market_select).select_by_value("sii")

            # 2. 輸入年度
            year_input = driver.find_element(By.ID, "year")
            year_input.clear()
            year_input.send_keys(str(year))

            # 3. 選擇季度（假設選項文字與 quarter 變數一致，如 "第一季"）
            # quarter_select = driver.find_element(By.ID, "season")
            # quarter_select.click()
            # quarter_option_xpath = f'//select[@id="season"]/option[text()="{quarter}"]'
            # wait.until(EC.element_to_be_clickable((By.XPATH, quarter_option_xpath)))
            # driver.find_element(By.XPATH, quarter_option_xpath).click()

            # 4. 點擊「查詢」按鈕
            query_button = driver.find_element(By.ID, "searchBtn")
            query_button.click()

            # 等待新視窗出現（查詢結果頁面通常以新視窗打開）
            wait.until(lambda d: len(d.window_handles) > 1)
            all_windows = driver.window_handles
            new_window = [w for w in all_windows if w != main_window][0]
            
            # 切換到新視窗，等待該視窗載入完成
            driver.switch_to.window(new_window)
            time.sleep(2)  # 根據實際情況調整

            current_url = driver.current_url
            print(f"取得 {year} {quarter} 的查詢結果頁連結: {current_url}")
            links.append((year, quarter, current_url))
            
            # 關閉新視窗，切回主視窗
            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(1)
    
    driver.quit()
    return links

def main():
    # 使用者輸入查詢頁面 URL（例如 MOPS 查詢頁面）
    #"https://mops.twse.com.tw/mops/#/web/t51sb02",
    web_list_url = ["https://mops.twse.com.tw/mops/#/web/t51sb02"]
    cleaned_urls = [url.strip() for url in web_list_url]
    print("清理後的查詢頁面 URL：", cleaned_urls)
    for web_url in web_list_url:
        main_url = web_url.strip()
        # 定義要查詢的年度與季度（請根據實際需求修改）
        years = list(range(102, 114))
        quarters = ["第一季"] #, "第二季", "第三季", "第四季"
        
        query_links = get_query_links(main_url, years, quarters)
        print("\n所有查詢結果連結 (年, 季, URL):")
        
        for item in query_links:
            print(f"item: {item}")
        
        # 接下來你可以把 query_links 傳給 downloader.py 處理下載
        for item in query_links:
            year, quarter, url = item
            start = url.find("ajax_")
            if start != -1:
                start += len("ajax_")
                end = url.find("?", start)
                if end == -1:
                    result = url[start:]
                else:
                    result = url[start:end]
                print("取出的字串:", result)
            else:
                print("找不到 'ajax_'")
            download_csv_folder=download_csv_files(f"{year}_{quarter}", url, result)
        
        # repair_csv_files(download_csv_folder)
        # repair_csv(download_csv_folder)

if __name__ == "__main__":
    main()