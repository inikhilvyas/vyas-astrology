import gdown
import os

url = 'https://drive.google.com/drive/folders/1lU6wQNPm6cK403OgbOvoizDlElVknkmV'
target_dir = 'books_downloaded'
os.makedirs(target_dir, exist_ok=True)

print("Running gdown folder download...")
# gdown.download_folder(url, output=target_dir, quiet=False, use_cookies=False)
try:
    files = gdown.download_folder(url, output=target_dir, quiet=False, use_cookies=False)
    print(f"Downloaded {len(files) if files else 0} files via gdown!")
except Exception as e:
    print(f"gdown error: {e}")

