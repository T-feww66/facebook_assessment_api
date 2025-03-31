from utils.find_filename_by_keyword import find_files_by_keyword

folder = "crawl_data/data/fanpages/"
word_search = "xiaomi"

matching_files = find_files_by_keyword(folder, word_search)
print("Các file phù hợp:", matching_files)