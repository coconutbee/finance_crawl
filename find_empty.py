import os

def find_empty_csv(folder):
    empty_csv_files = []
    # 遍歷資料夾中所有檔案
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = os.path.join(root, file)
                # 檢查檔案大小是否為 0
                if os.path.getsize(file_path) == 0:
                    empty_csv_files.append(file_path)
    return empty_csv_files

# 範例用法，請替換為你的資料夾路徑
folder_path = "twse_data"
empty_csvs = find_empty_csv(folder_path)

if empty_csvs:
    print("以下 CSV 檔案是空白的：")
    for csv_file in empty_csvs:
        print(csv_file)
else:
    print("沒有發現空白的 CSV 檔案。")
