import os
import shutil


def remove_cache_dirs(root_dir="."):
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)
                print(f"Removed: {cache_path}")


def remove_pytest_cache_dirs(root_dir="."):
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == ".pytest_cache":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)
                print(f"Removed: {cache_path}")


if __name__ == "__main__":
    remove_cache_dirs()
    remove_pytest_cache_dirs()
    print("Cache directories removed!")
