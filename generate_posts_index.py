import os
import json
import re
from datetime import datetime

MONTHS = ["СІЧ","ЛЮТ","БЕР","КВІ","ТРА","ЧЕР","ЛИП","СЕР","ВЕР","ЖОВ","ЛИС","ГРУ"]

def parse_markdown_meta(content):
    meta = {}
    match = re.match(r'---\n([\s\S]*?)\n---', content)
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip().strip('"')
    return meta

def generate_posts_index(posts_dir="posts", output_file="posts.json"):
    all_posts_meta = []
    
    if not os.path.exists(posts_dir):
        print(f"Error: Directory {posts_dir} not found.")
        return

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(posts_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping file {filename} due to error: {e}")
            continue

        meta = parse_markdown_meta(content)
        slug = filename.replace(".md", "")
        title = meta.get("title", "Без назви")
        excerpt = meta.get("excerpt", "")
        date_str = meta.get("date", "")
        tag = meta.get("tag", "Допис")

        display_date = "НОВЕ"
        if date_str:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d")
                display_date = f"{MONTHS[d.month - 1]}<br>{d.year}"
            except ValueError:
                pass

        all_posts_meta.append({
            "slug": slug,
            "title": title,
            "excerpt": excerpt,
            "date": date_str,
            "displayDate": display_date,
            "tag": tag
        })

    # Сортування: спочатку за датою, потім за назвою для стабільності
    all_posts_meta.sort(key=lambda x: (x.get('date', '0000-00-00'), x.get('slug', '')), reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_posts_meta, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_file} with {len(all_posts_meta)} posts.")

if __name__ == "__main__":
    generate_posts_index()
