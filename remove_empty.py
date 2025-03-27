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

if __name__ == "__main__":
    parent_folder = "Balance_Sheet_test"
    repair_csv(parent_folder)