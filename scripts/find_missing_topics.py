import json
import os
import sys

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
JSON_FILE = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 find_missing_topics.py <Theme Name or Index>")
        # Default to "神と経綸" for this specific user request if not provided, 
        # but better to force argument or handle gracefully.
        target_theme = "神と経綸"
    else:
        target_theme = sys.argv[1]

    if not os.path.exists(JSON_FILE):
        print(f"Error: File not found at {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get("themes", [])
    
    found_theme = None
    for theme in themes:
        if theme.get("theme_title") == target_theme or theme.get("theme_title_pt") == target_theme:
            found_theme = theme
            break
    
    if not found_theme:
        print(f"Theme '{target_theme}' not found.")
        return

    print(f"Analyzing missing topics for theme: {found_theme.get('theme_title')} ({found_theme.get('theme_title_pt')})")
    
    topics = found_theme.get("topics", [])
    missing_count = 0
    
    for idx, topic in enumerate(topics):
        if not topic.get("content_pt"):
            title = topic.get("title", "No Title")
            filename = topic.get("filename", "No Filename")
            print(f"- [Index {idx}] Title: {title} (File: {filename})")
            missing_count += 1

    print(f"\nTotal missing: {missing_count}")

if __name__ == "__main__":
    main()
