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

    if not os.path.isdir(folder_path):
        print(f"Thư mục không tồn tại: {folder_path}")
        return []

    file_list = glob.glob(os.path.join(folder_path, "*"))
    matching_files = [f for f in file_list if keyword in os.path.basename(f)]
    return matching_files