import os
from pypinyin import lazy_pinyin

def sort_entries(entries):
    """对条目按名字的拼音排序"""
    return sorted(entries, key=lambda x: lazy_pinyin(x[0]))

def save_to_file(name, url, is_fav, name_like_like, category):
    # 去除 URL 中的“这个来自”部分
    if "这个来自" in url:
        url = url.replace("这个来自", "").strip()

    # 根据条件选择文件名
    if is_fav:
        filename = "fav.txt"
    elif name_like_like:
        filename = "like.txt"
    else:
        # 根据分类选择文件名
        if category == "leg":
            filename = "leg.txt"
        elif category == "body":
            filename = "body.txt"
        elif category == "face":
            filename = "face.txt"
        else:
            filename = "data.txt"  # 默认文件

    # 确保文件存在
    if not os.path.exists(filename):
        open(filename, "w", encoding="utf-8").close()

    # 读取并更新内容
    entries = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    existing_name, existing_url = line.split(' ', 1)
                    entries.append((existing_name, existing_url))
                except ValueError:
                    print(f"Skipping malformed line: {line}")

    # 检查是否存在相同的名字
    if name in [entry[0] for entry in entries]:
        print("Name already exists.")
        return

    # 添加新条目并排序
    entries.append((name, url))
    sorted_entries = sort_entries(entries)

    # 将排序后的条目写回文件
    with open(filename, "w", encoding="utf-8") as file:
        for entry_name, entry_url in sorted_entries:
            file.write(f"{entry_name} {entry_url}\n")

    print(f"Entry added to {filename} and sorted by name.")

if __name__ == "__main__":
    while True:
        # 确保输入的 name 非空
        while True:
            name = input("Enter name: ").strip()
            if name:
                break
            print("Name cannot be empty. Please enter a valid name.")

        # 确保输入的 url 非空
        while True:
            url = input("Enter URL: ").strip()
            if url:
                break
            print("URL cannot be empty. Please enter a valid URL.")

        # 确保输入的 is_fav 非空
        while True:
            is_fav_input = input("Is this a favourite? (yes/no): ").strip().lower()
            if is_fav_input in ["yes", "no"]:
                is_fav = is_fav_input == "yes"
                break
            print("Please enter 'yes' or 'no'.")

        # 仅在 is_fav 为 no 时询问 name_like_like
        if not is_fav:
            while True:
                name_like_like_input = input("Do you 'like' this name? (yes/no): ").strip().lower()
                if name_like_like_input in ["yes", "no"]:
                    name_like_like = name_like_like_input == "yes"
                    break
                print("Please enter 'yes' or 'no'.")
        else:
            name_like_like = False  # 如果是 favourite，则自动设置 name_like_like 为 False

        # 确保输入的 category 非空并且在可选项中
        while True:
            category = input("Choose a category (leg/body/face): ").strip().lower()
            if category in ["leg", "body", "face"]:
                break
            print("Please enter a valid category: leg, body, or face.")

        save_to_file(name, url, is_fav, name_like_like, category)
