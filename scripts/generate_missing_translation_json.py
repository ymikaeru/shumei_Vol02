import json
import os
import math

# Configuration
INPUT_JSON = 'Data/shumeic1_part2_data_bilingual_fixed.json'
OUTPUT_DIR = 'Data/missing_parts_for_translation'
ITEMS_PER_FILE = 100

def main():
    if not os.path.exists(INPUT_JSON):
        print(f"Error: {INPUT_JSON} not found.")
        return

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    missing_topics = []
    
    for theme in data.get('themes', []):
        theme_title = theme.get('theme_title', '')
        for topic in theme.get('topics', []):
            if not topic.get('title_pt') or topic.get('title_pt').strip() == "":
                missing_topics.append({
                    "source_file": topic.get('filename', ''),
                    "theme_title": theme_title,
                    "title_jp": topic.get('title', ''),
                    "content_jp": topic.get('content', ''),
                    "publication_jp": topic.get('date', ''),
                    "title_ptbr": "",
                    "content_ptbr": ""
                })

    total_missing = len(missing_topics)
    print(f"Found {total_missing} missing topics.")
    
    if total_missing == 0:
        print("No missing topics found.")
        return

    # Split into files starting from missing_part_05.json
    num_files = math.ceil(total_missing / ITEMS_PER_FILE)
    
    for i in range(num_files):
        start = i * ITEMS_PER_FILE
        end = min((i + 1) * ITEMS_PER_FILE, total_missing)
        chunk = missing_topics[start:end]
        
        file_num = i + 5
        output_file = os.path.join(OUTPUT_DIR, f"missing_part_{file_num:02d}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        
        print(f"Generated {output_file} with {len(chunk)} items.")

if __name__ == "__main__":
    main()
