import json
import os
import glob

# Configuration
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01"
DATA_FILE = os.path.join(BASE_DIR, "Data/shumeic1_part2_data.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "Data/shumeic1_part2_data_bilingual.json")
OLD_TRANSLATIONS_DIR = os.path.join(BASE_DIR, "OldTraslations")

def normalize_text(text):
    """Normalize text for better matching (strip whitespace, etc)."""
    if not text:
        return ""
    return text.strip().replace("　", " ")

def clean_title(title):
    """
    Cleans the title by removing common prefixes and brackets.
    Ex: 明主様御講話　「大光明世界の建設」 -> 大光明世界の建設
    """
    if not title:
        return ""
    
    # Remove specific prefixes
    prefixes = ["明主様御講話", "明主様御講義", "明主様御教え", "明主様御垂示"]
    cleaned = title
    for p in prefixes:
        cleaned = cleaned.replace(p, "")
    
    # Remove brackets and extra spaces
    cleaned = cleaned.replace("「", "").replace("」", "").replace("　", " ").strip()
    return cleaned

def load_old_translations():
    """Loads all translations from OldTraslations directory into a lookup dict."""
    lookup = {}
    pattern = os.path.join(OLD_TRANSLATIONS_DIR, "*_merged.json")
    files = glob.glob(pattern)
    
    print(f"Loading translations from {len(files)} files...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            publications = data.get('publications', [])
            for pub in publications:
                jp_title = pub.get('publication_title')
                pt_title = pub.get('publication_title_ptbr')
                pt_content = pub.get('content_ptbr')
                
                # Check for alternative field names if primary ones are missing
                if not pt_title: pt_title = pub.get('title_ptbr')
                if not pt_content: pt_content = pub.get('content') # sometimes content is just content
                
                if jp_title and pt_title:
                    norm_title = normalize_text(jp_title)
                    entry = {
                        'title_pt': pt_title,
                        'content_pt': pt_content,
                        'source': os.path.basename(file_path)
                    }
                    lookup[norm_title] = entry
                    
                    if "（" in norm_title:
                        short_title = norm_title.split("（")[0].strip()
                        if short_title and short_title not in lookup:
                             lookup[short_title] = entry

        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return lookup

def ingest_translations():
    if not os.path.exists(DATA_FILE):
        print(f"Data file not found: {DATA_FILE}")
        return

    lookup = load_old_translations()
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
        
    themes = main_data.get('themes', [])
    updated_count = 0
    total_count = 0
    
    for theme in themes:
        topics = theme.get('topics', [])
        for topic in topics:
            total_count += 1
            jp_title = topic.get('title')
            
            # Matching Logic
            norm_title = normalize_text(jp_title)
            match = lookup.get(norm_title)
            
            if not match:
                cleaned = clean_title(jp_title)
                match = lookup.get(cleaned)
            
            if not match and "（" in norm_title:
                 short_title = norm_title.split("（")[0].strip()
                 match = lookup.get(short_title)
            
            # Ingest if found
            if match:
                topic['title_pt'] = match['title_pt']
                topic['content_pt'] = match['content_pt']
                
                # topic['translation_source'] = match['source'] # Optional metadata
                updated_count += 1

    # Save output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
        
    print("-" * 50)
    print(f"Total Topics: {total_count}")
    print(f"Updated with Old Translations: {updated_count}")
    print(f"Saved bilingual data to: {OUTPUT_FILE}")
    print("-" * 50)

if __name__ == "__main__":
    ingest_translations()
