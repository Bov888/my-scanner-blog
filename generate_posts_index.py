import os
import json
import re
from datetime import datetime

MONTHS = ["СІЧ","ЛЮТ","БЕР","КВІ","ТРА","ЧЕР","ЛИП","СЕР","ВЕР","ЖОВ","ЛИС","ГРУ"]

def parse_markdown_meta(content):
    meta = {}
    match = re.match(r'---\n([\s\S]*?)\n---', content)
    if not match:
        return meta
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip('"')
        # Мультизначення: [Tag1, Tag2] — розбираємо в масив
        if value.startswith('[') and value.endswith(']'):
            items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
            meta[key] = [i for i in items if i]
        else:
            meta[key] = value
    return meta

def generate_posts_index(posts_dir="posts", output_file="posts.json"):
    all_posts_meta = []

    if not os.path.exists(posts_dir):
        print(f"Error: Directory {posts_dir} not found.")
        return

    for filename in sorted(os.listdir(posts_dir)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(posts_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping {filename}: {e}")
            continue

        meta = parse_markdown_meta(content)
        slug = meta.get("slug") or filename.replace(".md", "")
        title = meta.get("title", "Без назви")
        excerpt = meta.get("excerpt", "")
        date_str = meta.get("date", "")

        # Теги: підтримуємо і один рядок ("tag") і масив ("tags")
        raw_tags = meta.get("tags") or meta.get("tag") or []
        if isinstance(raw_tags, str):
            raw_tags = [raw_tags]
        tags = [t.strip() for t in raw_tags if t.strip()]

        # Пов'язані дописи
        related = meta.get("related") or []
        if isinstance(related, str):
            related = [related]

        display_date = "НОВЕ"
        if date_str:
            try:
                d = datetime.strptime(date_str[:10], "%Y-%m-%d")
                display_date = f"{MONTHS[d.month - 1]}<br>{d.year}"
            except ValueError:
                pass

        all_posts_meta.append({
            "slug": slug,
            "title": title,
            "excerpt": excerpt,
            "date": date_str,
            "displayDate": display_date,
            "tags": tags,
            "related": related,
        })

    all_posts_meta.sort(
        key=lambda x: (x.get('date', '0000-00-00'), x.get('slug', '')),
        reverse=True
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_posts_meta, f, ensure_ascii=False, indent=2)

    print(f"Generated {output_file} with {len(all_posts_meta)} posts.")

if __name__ == "__main__":
    generate_posts_index()
