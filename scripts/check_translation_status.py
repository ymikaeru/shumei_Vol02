import json
import os

BASE_DIR = "Data"
JSON_FILE = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")

def main():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get("themes", [])
    total_topics = 0
    missing_count = 0
    
    print(f"Checking {len(themes)} themes for missing translations...\n")

    for t_idx, theme in enumerate(themes):
        theme_title = theme.get("theme_title", "Unknown")
        theme_title_pt = theme.get("theme_title_pt", "")
        
        topics = theme.get("topics", [])
        theme_missing = 0
        
        for topic in topics:
            total_topics += 1
            title_pt = topic.get("title_pt", "")
            content_pt = topic.get("content_pt", "")
            
            if not title_pt or not content_pt:
                missing_count += 1
                theme_missing += 1
                print(f"  Missing: {topic.get('filename', 'Unknown')}")

        if theme_missing > 0:
            print(f"Theme {t_idx + 1}: {theme_title} ({theme_title_pt})")
            print(f"  - Missing {theme_missing}/{len(topics)} topics")
            
    print("-" * 30)
    print(f"Total Topics: {total_topics}")
    print(f"Total Missing Translations: {missing_count}")
    print(f"Completion Rate: {((total_topics - missing_count) / total_topics) * 100:.2f}%")

if __name__ == "__main__":
    main()
