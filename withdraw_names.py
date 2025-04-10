import os
root = 'financial_data'
company_names = []

for file in os.listdir(root):
    if file=='Financial_Analysis':
        for subdir, _, files in os.walk(os.path.join(root, file)):
            for file_csv in files:
                # print(file_csv)
                if file_csv.endswith('.csv'):
                    # print(os.path.join(subdir, file_csv))
                    with open(os.path.join(subdir, file_csv), 'r', encoding="utf-8") as f:
                        lines = f.readlines()
                        for line in lines[1:]:
                            fields = line.strip().split(',')
                            if len(fields) > 3:
                                # 假設第5個欄位(索引 4)代表公司名稱
                                name = fields[0].replace('"', '')
                                ccname = fields[1].replace('"', '').replace('*', '')
                                print(name, ccname)
                                name = f"{name}_{ccname}"
                                company_names.append(name)
                                

                # if not os.path.exists(os.path.join('test')):
                #     os.makedirs(os.path.join('test'))
                # with open(os.path.join('test', file_csv), 'w', encoding='utf-8') as f:
                #     f.writelines(lines)
# print('公司名稱數量:', len(company_names))
# print('公司名稱:', company_names)
with open('company_names.txt', 'a', encoding='utf-8') as f:
    for names in set(company_names):
        f.write(names + '\n')
print('公司名稱已寫入 company_names.txt')
