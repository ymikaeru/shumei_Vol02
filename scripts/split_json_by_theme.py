import json
import os
import re

# Logic from implementation plan
# 1. Load the main JSON file.
# 2. Iterate through themes.
# 3. Save each theme as a separate JSON file.

INPUT_FILE = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/shumeic1/shumeic1_part2_data.json"
OUTPUT_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/shumeic1/split_parts"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>| ]', "_", name)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get('themes', [])
    print(f"Found {len(themes)} themes.")

    for i, theme in enumerate(themes):
        theme_title = theme.get('theme_title', f"Theme_{i+1}")
        safe_title = clean_filename(theme_title)
        
        # Construct filename
        # Using 02d for sorting
        filename = f"theme_{i+1:02d}_{safe_title}.json"
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        # Prepare content for this file
        # We might want to keep the volume title in each part for context
        part_data = {
            "volume_title": data.get('volume_title', ""),
            "theme_title": theme_title,
            "topics": theme.get('topics', [])
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(part_data, f, ensure_ascii=False, indent=2)
            
        print(f"Saved: {filename}")

if __name__ == "__main__":
    main()
