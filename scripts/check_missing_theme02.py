
import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
JSON_FILE = os.path.join(BASE_DIR, "shumeic2_data_bilingual.json")

def main():
    if not os.path.exists(JSON_FILE):
        print(f"Error: File not found at {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get("themes", [])
    
    target_theme_title = "浄霊の方法"
    found_theme = None
    
    for theme in themes:
        if theme.get("theme_title") == target_theme_title:
            found_theme = theme
            break
            
    if not found_theme:
        print(f"Theme '{target_theme_title}' not found.")
        return

    print(f"Checking missing translations for: {found_theme.get('theme_title')} ({found_theme.get('theme_title_pt')})")
    
    topics = found_theme.get("topics", [])
    missing_count = 0
    
    for idx, topic in enumerate(topics):
        if not topic.get("title_pt") or not topic.get("content_pt"):
            print(f"- [Index {idx}] File: {topic.get('filename')} | Title: {topic.get('title')}")
            missing_count += 1

    print(f"\nTotal missing: {missing_count}")

if __name__ == "__main__":
    main()
