import os
import json
import re
from datetime import datetime

def parse_markdown_meta(content):
    meta = {}
    # Regex to find YAML front matter
    match = re.match(r'''---
([\s\S]*?)
---''', content)
    if match:
        front_matter = match.group(1)
        # ВИПРАВЛЕНО: Використовуємо splitlines() для надійного розбиття рядка на окремі рядки.
        for line in front_matter.splitlines(): 
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip().strip('"')
    return meta

def generate_posts_index(posts_dir="posts", output_file="posts.json"):
    all_posts_meta = []
    
    # Define Ukrainian month names for date formatting
    MONTHS_UA = [
        "січня", "лютого", "березня", "квітня", "травня", "червня",
        "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"
    ]

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                meta = parse_markdown_meta(content)
                
                slug = filename.replace(".md", "")
                title = meta.get("title", "Без назви")
                excerpt = meta.get("excerpt", "")
                date_str = meta.get("date", "")
                tag = meta.get("tag", "Допис")

                display_date = "НОВЕ"
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        display_date = f"{MONTHS_UA[date_obj.month - 1]}<br>{date_obj.year}"
                    except ValueError:
                        pass # Keep "НОВЕ" if date parsing fails
                
                all_posts_meta.append({
                    "slug": slug,
                    "title": title,
                    "excerpt": excerpt,
                    "date": date_str,
                    "displayDate": display_date,
                    "tag": tag
                })
    
    # Sort posts by date, newest first
    all_posts_meta.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_posts_meta, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_posts_index()
