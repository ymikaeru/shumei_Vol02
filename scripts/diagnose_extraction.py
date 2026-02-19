
import json
import os
import re

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
MAIN_JSON = 'Data/shumeic1_part2_data_bilingual_repaired.json'

def main():
    if not os.path.exists(MAIN_JSON):
        print("Error: Bilingual JSON not found.")
        return

    with open(MAIN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    truncated_candidates = []
    
    if "themes" in data:
        for theme in data["themes"]:
            for topic in theme.get("topics", []):
                content_jp = topic.get("content", "")
                filename = topic.get("filename", "")
                title = topic.get("title", "")
                
                # Check for truncation (failure to reach <hr>)
                # Note: The last topic in a file might not have an <hr> in the source, 
                # but our extractor usually adds it or stops at </BLOCKQUOTE>.
                if content_jp and "<hr" not in content_jp.lower():
                    truncated_candidates.append({
                        "filename": filename,
                        "title": title,
                        "issue": "Missing <hr/> tag"
                    })

    print(f"Extraction Audit: Found {len(truncated_candidates)} potentially truncated items (no <hr/>).")
    print("-" * 50)
    for item in truncated_candidates[:30]:
        print(f"{item['filename']} | {item['title']}")
    
    if len(truncated_candidates) > 30:
        print(f"... and {len(truncated_candidates) - 30} more.")

if __name__ == "__main__":
    main()
