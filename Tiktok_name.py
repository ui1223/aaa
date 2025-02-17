import os
from pypinyin import lazy_pinyin

# 分类列表
CATEGORIES = ["leg", "body", "face", "COS", "music", "youth", "Joker", "cloth", "dance", "team", "Photo"]

def sort_entries(entries):
    """对条目按名字的拼音排序"""
    return sorted(entries, key=lambda x: lazy_pinyin(x[0]))

def check_name_exists(name):
    """检查名字是否已存在于所有分类文件中"""
    filenames = ["fav.txt", "like.txt", "data.txt"] + [f"{category}.txt" for category in CATEGORIES]
    for filename in filenames:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    existing_name = line.strip().split(' ', 1)[0]
                    if existing_name == name:
                        return True
    return False

def clean_url(url):
    """清理URL中的指定文本内容"""
    return url.replace("这个来自", "").replace(
        "长按复制此条消息，打开抖音搜索，查看TA的更多作品。", "").strip()

def get_valid_category():
    """从用户输入中获取有效的分类，返回标准化的分类名称"""
    while True:
        category_input = input(f"Choose a category ({'/'.join(CATEGORIES)}): ").strip().lower()
        if category_input == 'exit':
            print("Skipping category selection.")
            return None
        category = next((c for c in CATEGORIES if c.lower() == category_input), None)
        if category:
            return category
        print(f"Please enter a valid category or type 'exit' to skip: {', '.join(CATEGORIES)}.")

def get_user_input():
    """获取用户输入的 name, url, is_fav, name_like_like, 和 category"""
    while True:
        name = input("Enter name (or 'exit' to skip): ").strip()
        if name == 'exit':
            print("Skipping entry.")
            return None, None, None, None, None
        if name:
            if check_name_exists(name):
                print("Name already exists in one of the files.")
                continue
            break
        print("Name cannot be empty. Please enter a valid name.")

    url = input("Enter URL (or 'exit' to skip): ").strip()
    if url == 'exit':
        print("Skipping entry.")
        return None, None, None, None, None
    url = clean_url(url) if url else None
    if not url:
        print("URL cannot be empty.")
        return get_user_input()

    is_fav = input("Is this a favourite? (yes/no/exit): ").strip().lower()
    if is_fav == 'exit':
        print("Skipping entry.")
        return None, None, None, None, None
    is_fav = is_fav == "yes"

    name_like_like = False
    category = None

    if not is_fav:
        name_like_like_input = input("Do you 'like' this name? (yes/no/exit): ").strip().lower()
        if name_like_like_input == 'exit':
            print("Skipping entry.")
            return None, None, None, None, None
        name_like_like = name_like_like_input == "yes"
        if name_like_like:
            category = get_valid_category()

    return name, url, is_fav, name_like_like, category

def save_to_file(name, url, is_fav, name_like_like, category):
    # 确定保存的文件名
    if is_fav:
        filename = "fav.txt"
    elif name_like_like:
        filename = f"{category}.txt" if category else "like.txt"
    else:
        filename = "data.txt"

    # 获取现有条目并检查重复
    entries = []
    with open(filename, "a+", encoding="utf-8") as file:
        file.seek(0)
        entries = [line.strip().split(' ', 1) for line in file if line.strip()]
        if name in (entry[0] for entry in entries):
            print(f"Entry '{name}' already exists in {filename}.")
            return

        # 添加新条目并排序
        entries.append((name, url))
        entries = sort_entries(entries)

        # 重写文件内容
        file.seek(0)
        file.truncate(0)
        for entry_name, entry_url in entries:
            file.write(f"{entry_name} {entry_url}\n")

    print(f"Entry added to {filename} and sorted by name.")

if __name__ == "__main__":
    while True:
        user_input = get_user_input()
        if any(user_input):
            name, url, is_fav, name_like_like, category = user_input
            save_to_file(name, url, is_fav, name_like_like, category)
        else:
            print("Skipping current entry due to exit command.")



