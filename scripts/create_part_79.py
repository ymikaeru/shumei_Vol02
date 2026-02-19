
import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
SOURCE_JSON = os.path.join(BASE_DIR, "shumeic2_data.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "translated_parts", "theme_02_浄霊の方法_part_79.json")

TARGET_TITLES = [
    "明主様御講話　「胃病患者は肩が張っている」",
    "明主様御講話　「中風患者は首のまわりに固まりがある」",
    "明主様御講話　「息切れの浄霊の急所」",
    "明主様御垂示　「腹部膨満による排尿困難に対する浄霊の急所」",
    "明主様御垂示　「胃癌患者に対して肩を中心に浄霊すべきとした事例」",
    "明主様御垂示　「狂犬病の浄霊の急所」",
    "明主様御垂示　「チフスの浄霊の急所」",
    "明主様御垂示　「毒で自殺した霊の憑依による筋肉萎縮硬化症に対する浄霊の急所」",
    "明主様御垂示　「色盲の浄霊の急所」"
]

def main():
    if not os.path.exists(SOURCE_JSON):
        print(f"Error: Source file not found at {SOURCE_JSON}")
        return

    print(f"Loading {SOURCE_JSON}...")
    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find Theme 02
    target_theme = None
    for theme in data.get("themes", []):
        if theme.get("theme_title") == "浄霊の方法":
            target_theme = theme
            break
    
    if not target_theme:
        print("Error: Theme '浄霊の方法' not found.")
        return

    extracted_items = []
    
    # Iterate through topics and find matches
    topics = target_theme.get("topics", [])
    print(f"Scanning {len(topics)} topics...")
    
    found_count = 0
    
    for topic in topics:
        title = topic.get("title", "").strip()
        filename = topic.get("filename", "")
        
        if title in TARGET_TITLES:
            print(f"Found: {title}")
            
            # Create the item structure for the part file
            # We populate ptbr fields with Japanese content as placeholders/source for translation
            item = {
                "source_file": filename,
                "title_ptbr": title, # Keeping Japanese title temporarily
                "content_ptbr": topic.get("content", ""), # Keeping Japanese content
                "publication_title_ptbr": ""
            }
            extracted_items.append(item)
            found_count += 1

    if found_count == 0:
        print("Warning: No topics found matching the target titles.")
    else:
        print(f"Extracted {found_count} topics.")

    # Sort if necessary, but preserving order is usually better. 
    # The order in TARGET_TITLES might be different from source order. 
    # Current loop preserves source order.

    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(extracted_items, f, indent=2, ensure_ascii=False)
    
    print("Done.")

if __name__ == "__main__":
    main()
