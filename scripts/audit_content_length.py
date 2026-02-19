
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

    short_items = []
    # Threshold for "potentially truncated" content.
    # 300 characters is roughly a very short paragraph including HTML tags.
    THRESHOLD = 300 

    if "themes" in data:
        for theme in data["themes"]:
            for topic in theme.get("topics", []):
                content_jp = topic.get("content", "")
                # Clean HTML tags to count actual text? 
                # Or just count the whole thing? HTML tags are part of the content here.
                length = len(content_jp)
                
                if length > 0 and length < THRESHOLD:
                    short_items.append({
                        "filename": topic.get("filename"),
                        "title": topic.get("title"),
                        "length": length,
                        "content_preview": content_jp[:100].replace("\n", " ")
                    })

    # Sort by length ascending
    short_items.sort(key=lambda x: x["length"])

    print(f"Audit Results: Found {len(short_items)} items with content length < {THRESHOLD}")
    print("-" * 50)
    for item in short_items[:50]: # Show first 50
        print(f"Length {item['length']} | {item['filename']} | {item['title']}")
        # print(f"Preview: {item['content_preview']}...")
    
    if len(short_items) > 50:
        print(f"... and {len(short_items) - 50} more.")

if __name__ == "__main__":
    main()
