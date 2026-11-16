import os
import re

root = r"g:\software\simpa\VYAS"
mob_path = os.path.join(root, "mobile", "index.html")
app_path = os.path.join(root, "android_app", "app", "src", "main", "assets", "mobile", "index.html")

for path in [mob_path, app_path]:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Match the 1-click install banner
    pattern = r'<!-- 1-Click Install Banner -->\s*<div class="m-card"[^>]*>[\s\S]*?</div>\s*</div>'
    match = re.search(pattern, text)
    if match:
        text = re.sub(pattern, '', text)
        print(f"Removed install banner from {path}")
    else:
        # Fallback search
        pattern2 = r'<div class="m-card"[^>]*>\s*<div>\s*<b[^>]*>मोबाइल ऐप इंस्टॉल करें[\s\S]*?</div>\s*</div>'
        if re.search(pattern2, text):
            text = re.sub(pattern2, '', text)
            print(f"Removed install banner via pattern2 from {path}")
        else:
            print(f"Banner not found in {path}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

print("Done updating files!")

