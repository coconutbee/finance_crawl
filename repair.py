import os
import shutil

# 若 error_path 目錄不存在，先建立
def repair_csv_files(root):
    error_path = "error_path"
    if not os.path.exists(error_path):
        os.makedirs(error_path)

    for _, subdirs, files in os.walk(root):
        for file in subdirs:
            csv_dir = os.path.join(root, file)
            print(f"目前處理的資料夾: {csv_dir}")
            for csv_file in os.listdir(csv_dir):
                ori = os.path.join(csv_dir, csv_file)
                print(csv_file)   
                print(f"處理檔案: {ori}")
                # 讀取目前錯誤的 UTF-8 檔案（內容其實是先前錯誤解碼後的結果）
                # 改為以二進位模式讀取檔案
                with open(ori, 'rb') as f:
                    raw_bytes = f.read()

                # 先用 iso-8859-1 解碼，這樣可以獲得一個中間的字串
                garbled_text = raw_bytes.decode("iso-8859-1", errors="replace")

                # 嘗試用 big5 解碼這個字串（先把它重新編碼回 iso-8859-1 的 bytes，再用 big5 解碼）
                try:
                    repaired_text = garbled_text.encode("iso-8859-1").decode("big5", errors="replace")
                except Exception as e:
                    print("big5 解碼失敗，嘗試 cp950...")
                    try:
                        repaired_text = garbled_text.encode("iso-8859-1").decode("cp950", errors="replace")
                    except Exception as e:
                        print("cp950 解碼失敗，錯誤訊息：", e)
                        repaired_text = None

                # 若成功解碼，就存成 UTF-8 格式的檔案
                if repaired_text is not None:
                    with open(ori, "w", encoding="utf-8-sig") as f:
                        f.write(repaired_text)
                    # print(f"{ori} 修復成功！")
                else:
                    print(f"{ori} 檔案修復失敗，將檔案搬移到 error_path")
                    shutil.move(ori, os.path.join("error_path", os.path.basename(ori)))


if __name__ == "__main__":
    root = "Financial_Analysis"
    repair_csv_files(root)