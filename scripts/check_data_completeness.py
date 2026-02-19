
import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
MAIN_JSON = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")

def main():
    if not os.path.exists(MAIN_JSON):
        print("Error: Bilingual JSON not found.")
        return

    with open(MAIN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_topics = 0
    missing_jp_title = 0
    missing_jp_content = 0
    missing_pt_title = 0
    missing_pt_content = 0
    
    missing_items = []

    if "themes" in data:
        for theme in data["themes"]:
            for topic in theme.get("topics", []):
                total_topics += 1
                
                title_jp = topic.get("title", "").strip()
                content_jp = topic.get("content", "").strip()
                title_pt = topic.get("title_pt", "").strip()
                content_pt = topic.get("content_pt", "").strip()
                
                issues = []
                if not title_jp:
                    missing_jp_title += 1
                    issues.append("Missing JP Title")
                if not content_jp:
                    missing_jp_content += 1
                    issues.append("Missing JP Content")
                
                if not title_pt:
                    missing_pt_title += 1
                    issues.append("Missing PT Title")
                if not content_pt:
                    missing_pt_content += 1
                    issues.append("Missing PT Content")
                
                if issues:
                    missing_items.append({
                        "filename": topic.get("filename", "unknown"),
                        "title": title_jp,
                        "date": topic.get("date", ""),
                        "issues": issues
                    })

    print(f"Total Topics Scanned: {total_topics}")
    print("-" * 30)
    print(f"Missing Japanese Title: {missing_jp_title}")
    print(f"Missing Japanese Content: {missing_jp_content}")
    print(f"Missing Portuguese Title: {missing_pt_title}")
    print(f"Missing Portuguese Content: {missing_pt_content}")
    print("-" * 30)
    
    if missing_items:
        print("\nDetails of missing items (first 10):")
        for item in missing_items[:10]:
            print(f"- {item['filename']} | {item['title']} | {item['date']} -> {', '.join(item['issues'])}")
        
        if len(missing_items) > 10:
            print(f"... and {len(missing_items) - 10} more.")
    else:
        print("\nPerfect! No missing content found.")

if __name__ == "__main__":
    main()
