import os
from pdf_processor import scan_directory


if __name__ == "__main__":
    watch_dir = os.getcwd()
    print(f"Watching directory: {watch_dir}")

    for log in scan_directory(watch_dir):
        print(log)
