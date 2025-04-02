import os
# 取得當前目錄下所有 CSV 檔案
def repair_csv(parent_folder):
    for parent, subdirs, files in os.walk(parent_folder):
        for file in files:
            csv_files = os.path.join(parent, file)
            # print(csv_files)
            with open(csv_files, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                filtered_lines = [line for line in lines if line.strip()]
            with open(csv_files, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
                print(f"{csv_files} 已處理完畢，移除空白列。")
def remove_special_line(parent_folder):
    # 如果輸出資料夾不存在，先建立
    # output_folder = "output"
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    
    # 遍歷 parent_folder 中的所有檔案
    for parent, subdirs, files in os.walk(parent_folder):
        for file in files:
            # 僅處理 .csv 檔案（不區分大小寫）
            if not file.lower().endswith(".csv"):
                continue
            
            # 取得原始 csv 檔案完整路徑
            csv_path = os.path.join(parent, file)
            
            # 產生輸出檔案的完整路徑，
            # 這裡直接將檔案寫入 output_folder，檔名保持不變
            
            # output_path = os.path.join(output_folder, parent, file)
            # if not os.path.exists(os.path.join(output_folder, parent)):
            #     os.makedirs(os.path.join(output_folder, parent))
            print(f"處理檔案: {csv_path}")
            
            # 讀取原始檔案內容
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 定義需要刪除行的關鍵字
            key_words = ["說明", "當日統計", "外幣成交值"]
            
            # 過濾掉包含任一關鍵字的行
            filtered_lines = [line for line in lines if not any(keyword in line for keyword in key_words)]
            
            # 寫入處理後的內容到 output_path
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
            
        print(f"csv去除特定列，處理完畢")
if __name__ == "__main__":
    parent_folder = "twse_data"
    # repair_csv(parent_folder)
    remove_special_line(parent_folder)