import os
import glob

def find_files_by_keyword(folder_path: str, keyword: str):
    """
    Tìm các file trong thư mục có chứa keyword trong tên.

    Args:
        folder_path (str): Đường dẫn thư mục chứa file.
        keyword (str): Từ khóa cần tìm trong tên file.

    Returns:
        list: Danh sách các file phù hợp.
    """
    file_list = glob.glob(os.path.join(folder_path, "*"))
    matching_files = [f for f in file_list if keyword in os.path.basename(f)]
    return matching_files


# Thư mục chứa file
folder = "crawl_data/data/fanpages/"
word_search = "xiaomi"

# Tìm kiếm file phù hợp
matching_files = find_files_by_keyword(folder, word_search)

# In kết quả
print("Các file phù hợp:", matching_files)
