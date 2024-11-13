import os
from pypinyin import lazy_pinyin

def sort_entries(entries):
    """对条目按名字的拼音排序"""
    return sorted(entries, key=lambda x: lazy_pinyin(x[0]))

def check_name_exists(name):
    """检查名字是否已存在于所有分类文件中"""
    filenames = ["fav.txt", "like.txt", "leg.txt", "body.txt", "face.txt", 
                 "COS.txt", "music.txt", "youth.txt", "Joker.txt",
                 "Num5.txt", "Num6.txt", "Num7.txt", "Num8.txt", "data.txt"]
    for filename in filenames:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    existing_name = line.strip().split(' ', 1)[0]
                    if existing_name == name:
                        return True
    return False

def save_to_file(name, url, is_fav, name_like_like, category):
    # 去除 URL 中的指定文本
    url = url.replace("长按复制此条消息，打开抖音搜索，查看TA的更多作品。", "").strip()

    # 根据条件选择文件名
    if is_fav:
        filename = "fav.txt"
    elif name_like_like:
        filename = "like.txt"
        # 如果有分类，进一步决定文件名
        if category:
            filename = f"{category}.txt"
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
                # 检查名字是否在所有文件中已存在
                if check_name_exists(name):
                    print("Name already exists in one of the files.")
                    continue
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
            # 确保输入的 name_like_like 非空
            while True:
                name_like_like_input = input("Do you 'like' this name? (yes/no): ").strip().lower()
                if name_like_like_input in ["yes", "no"]:
                    name_like_like = name_like_like_input == "yes"
                    break
                print("Please enter 'yes' or 'no'.")

            # 仅在 name_like_like 为 yes 时询问 category
            if name_like_like:
                while True:
                    category = input("Choose a category (leg/body/face/COS/music/youth/Joker/Num5/Num6/Num7/Num8): ").strip().lower()
                    if category in ["leg", "body", "face", "cos", "music", "youth", "joker", "num5", "num6", "num7", "num8"]:
                        category = category.capitalize()  # 将分类转为首字母大写以匹配文件名
                        break
                    print("Please enter a valid category: leg, body, face, COS, music, youth, Joker, Num5, Num6, Num7, or Num8.")
            else:
                category = None  # 没有分类
        else:
            name_like_like = False  # 如果是 favourite，则自动设置 name_like_like 为 False
            category = None  # 不需要分类

        save_to_file(name, url, is_fav, name_like_like, category)
