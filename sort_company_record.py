import os

# ----------------------------
# 依據各子資料夾處理 CSV 檔案
# ----------------------------
# 針對 root 底下每個子資料夾進行處理，每個子資料夾的資料有各自不同的 header
def find_company_data(root, company_code, output_file):
    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)
        if os.path.isdir(folder_path):
            header_written = False  # 每個子資料夾內第一個含 header 的 CSV 檔案都需先寫入 header
            # ----------------------------
            # 遍歷子資料夾內的所有 CSV 檔案
            # ----------------------------
            for subdir, _, files in os.walk(folder_path):
                for file_csv in files:
                    if file_csv.endswith('.csv'):
                        csv_path = os.path.join(subdir, file_csv)
                        # print("正在處理檔案：", csv_path)
                        with open(csv_path, 'r', encoding='utf-8-sig') as f:
                            lines = f.readlines()
                        if not lines:
                            continue
                        header = [field.replace('"', '').strip() for field in lines[0].strip().split(',')]
                        # print("檔案 {} 的 header：".format(file_csv), header)
                        # ----------------------------
                        # 檢查 header 並找出 "公司代號" 欄位
                        # ----------------------------
                        if "公司代號" in header:
                            company_code_idx = header.index("公司代號")
                            # ----------------------------
                            # 寫入該子資料夾的 header (僅第一次出現時)
                            # ----------------------------
                            if not header_written:
                                # 為了明確區分，先加入一行提示來自哪個子資料夾，再寫入 header
                                header_line = f"{folder}歷史資料\n" + lines[0].strip()
                                with open(output_file, 'a', encoding='utf-8') as out_f:
                                    out_f.write(header_line + '\n')
                                header_written = True

                            # ----------------------------
                            # 處理該 CSV 檔案的資料列
                            # ----------------------------
                            for line in lines[1:]:
                                fields = line.strip().split(',')
                                if len(fields) > company_code_idx:
                                    field_code = fields[company_code_idx].replace('"', '')
                                    if company_code == field_code:
                                        # print("找到資料：", line.strip())
                                        with open(output_file, 'a', encoding='utf-8') as out_f:
                                            out_f.write(line.strip() + '\n')
                        else:
                            print("檔案 {0} 的標題列中沒有 '公司代號' 欄位".format(file_csv))



def get_company_code():
    with open('company_names.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        company_info = [line.strip() for line in lines if line.strip()]
        print(company_info)
    return company_info

if __name__ == "__main__":
    root = 'financial_data'                     # 來源資料夾，包含多個子資料夾
    target_folder = 'n8n_RAG'                     # 輸出結果的資料夾
    company_info = get_company_code()  # 取得公司代號
    for company in company_info:
        output_file = os.path.join(target_folder, f"{company}.csv")
        company_code = company.split('_')[0]  
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        find_company_data(root, company_code, output_file)