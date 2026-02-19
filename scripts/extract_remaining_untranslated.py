
import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
INPUT_FILE = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "remaining_untranslated.json")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    missing_translations = []

    print(f"Scanning {INPUT_FILE}...")
    
    total_topics = 0
    missing_count = 0

    if "themes" in data:
        for theme in data["themes"]:
            theme_title = theme.get("theme_title", "Unknown Theme")
            if "topics" in theme:
                for topic in theme["topics"]:
                    total_topics += 1
                    
                    # Check if translated content exists and is not empty
                    content_pt = topic.get("content_pt", "").strip()
                    title_pt = topic.get("title_pt", "").strip()
                    
                    # Criteria for "needs translation":
                    # Content is empty OR Title is empty (assuming translation implies both)
                    # Adjust based on user needs. Usually content is the main one.
                    
                    if not content_pt:
                        # Add metadata for context
                        entry = topic.copy()
                        entry["_theme_context"] = theme_title
                        missing_translations.append(entry)
                        missing_count += 1

    output_data = {
        "count": missing_count,
        "topics": missing_translations
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Total topics scanned: {total_topics}")
    print(f"Topics needing translation: {missing_count}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
