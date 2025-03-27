# 專案說明

此專案包含兩個主要的爬蟲程式：
1. `crawl.py` 用於爬取 [MOPS](https://mops.twse.com.tw/mops/#/Web/home) 網站提供的投資法人資料。
2. `TWSE_crawl.py` 用於爬取 [TWSE](https://www.twse.com.tw/zh/trading/historical/fmtqik.html) 每日的歷史數據。

---

## 環境設置

1. 建立並啟用虛擬環境
   ```bash
   python -m venv .venv
   .venv/Scripts/activate

2. 安裝所需套件
   ```bash
   pip install -r requirements.txt

## 使用方式
1. 執行 crawl.py 以爬取 MOPS 投資法人資料
2. 執行 TWSE_crawl.py 以爬取 TWSE 每日歷史數據