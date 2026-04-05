import os
import json
import re

def parse_meta(content, key):
    match = re.search(f"{key}:\\s*\"?([^\"\\n]+)\"?", content)
    return match.group(1).strip() if match else ""

posts_dir = "posts"
posts_list = []

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        with open(os.path.join(posts_dir, filename), "r", encoding="utf-8") as f:
            content = f.read()
            slug = filename.replace(".md", "")
            
            posts_list.append({
                "slug": slug,
                "title": parse_meta(content, "title"),
                "date": parse_meta(content, "date"),
                "tag": parse_meta(content, "tag"),
                "excerpt": parse_meta(content, "excerpt")
            })

# Сортування: новіші дописи зверху
posts_list.sort(key=lambda x: x['date'], reverse=True)

with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts_list, f, ensure_ascii=False, indent=2)

print(f"Успішно оновлено posts.json. Знайдено дописів: {len(posts_list)}")
