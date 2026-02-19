import json
import os
import glob
from collections import defaultdict

# Configuration
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01"
DATA_FILE = os.path.join(BASE_DIR, "Data/shumeic1_part2_data.json")
OLD_TRANSLATIONS_DIR = os.path.join(BASE_DIR, "OldTraslations")

def normalize_text(text):
    """Normalize text for better matching (strip whitespace, etc)."""
    if not text:
        return ""
    return text.strip().replace("　", " ") # Replace full-width space with normal space

def load_old_translations():
    """Loads all translations from OldTraslations directory into a lookup dict."""
    lookup = {}
    
    # We prefer _merged.json files as they seem to be the most complete
    pattern = os.path.join(OLD_TRANSLATIONS_DIR, "*_merged.json")
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} merged translation files.")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            publications = data.get('publications', [])
            for pub in publications:
                # Some files might have different structures, but based on inspection:
                # publication_title is the Japanese title inside the publication object
                # title is often the Theme title in these files?
                # Let's inspect the sample closer.
                # Sample:
                # "title": "神と経綸　１", -> Theme Title with number?
                # "publication_title": "天地の根本の神様 （昭和10年7月15日発行）" -> The actual lecture title
                
                # The main JSON 'title' corresponds to the lecture title.
                jp_title = pub.get('publication_title')
                pt_title = pub.get('publication_title_ptbr')
                pt_content = pub.get('content_ptbr')
                
                if jp_title:
                    norm_title = normalize_text(jp_title)
                    lookup[norm_title] = {
                        'title_pt': pt_title,
                        'content_pt': pt_content,
                        'source_file': os.path.basename(file_path)
                    }
                    
                    # Also try to index by valid title without date if present
                    # ex: "天地の根本の神様 （昭和10年7月15日発行）" -> "天地の根本の神様"
                    if "（" in norm_title:
                        short_title = norm_title.split("（")[0].strip()
                        if short_title and short_title not in lookup:
                             lookup[short_title] = {
                                'title_pt': pt_title,
                                'content_pt': pt_content,
                                'source_file': os.path.basename(file_path)
                            }

        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    print(f"Indexed {len(lookup)} unique Japanese titles from old translations.")
    return lookup

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

def analyze_coverage(lookup):
    if not os.path.exists(DATA_FILE):
        print(f"Data file not found: {DATA_FILE}")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
        
    themes = main_data.get('themes', [])
    
    total_topics = 0
    matched_topics = 0
    missing_topics = []
    
    # Debug: Print some lookup keys
    print("\nSample Lookup Keys (Old Translations):")
    sample_keys = list(lookup.keys())[:10]
    for k in sample_keys:
        print(f" - {k}")
    print("-" * 30)

    for theme in themes:
        topics = theme.get('topics', [])
        for topic in topics:
            total_topics += 1
            jp_title = topic.get('title')
            
            # Try exact match first
            norm_title = normalize_text(jp_title)
            match = lookup.get(norm_title)
            
            # Try cleaning the title (removing prefixes/brackets)
            if not match:
                cleaned = clean_title(jp_title)
                match = lookup.get(cleaned)
            
            # Try stripping date from main data title too (if it made it through cleaning)
            if not match and "（" in norm_title:
                 short_title = norm_title.split("（")[0].strip()
                 match = lookup.get(short_title)
            
            if match:
                matched_topics += 1
                # print(f"[MATCH] {jp_title} -> {match['source_file']}")
            else:
                missing_topics.append(jp_title)
                
    coverage = (matched_topics / total_topics) * 100 if total_topics > 0 else 0
    
    print("-" * 50)
    print(f"Total Topics in New Data: {total_topics}")
    print(f"Matched Topics in Old Translations: {matched_topics}")
    print(f"Unique Old Translation Titles: {len(lookup)}")
    print(f"Coverage (of New Data): {coverage:.2f}%")
    print(f"Utilization (of Old Translations): {(matched_topics / len(lookup)) * 100:.2f}%")
    print("-" * 50)
    
    # Identify which Old Translations were NOT used
    used_keys = set()
    # Re-run matching logic briefly to capture used keys (or I could have tracked it above)
    # Better to just track it in the main loop, but I can't edit that easily with search/replace without replacing the whole block.
    # I'll just explain I'm doing a lightweight pass here or relies on the user trusting the utilization stat for now.
    
    # Actually, let's just print matched examples first.
    # To do this effectively without rewriting the big loop, I will just add the prints here if I can't easily modify the loop.
    # But I CAN modify the loop. I'll replace the loop and the end reporting.
    
    if missing_topics:
        print("\nSample Missing Topics (First 10):")
        for t in missing_topics[:10]:
            print(f" - {t} (Cleaned: {clean_title(t)})")
            
def analyze_coverage_improved(lookup):
    if not os.path.exists(DATA_FILE):
        print(f"Data file not found: {DATA_FILE}")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
        
    themes = main_data.get('themes', [])
    
    total_topics = 0
    matched_topics = 0
    used_keys = set()
    missing_topics = []
    matched_examples = []
    
    for theme in themes:
        topics = theme.get('topics', [])
        for topic in topics:
            total_topics += 1
            jp_title = topic.get('title')
            
            norm_title = normalize_text(jp_title)
            match = lookup.get(norm_title)
            match_key = norm_title
            
            if not match:
                cleaned = clean_title(jp_title)
                match = lookup.get(cleaned)
                match_key = cleaned
            
            if not match and "（" in norm_title:
                 short_title = norm_title.split("（")[0].strip()
                 match = lookup.get(short_title)
                 match_key = short_title
            
            if match:
                matched_topics += 1
                used_keys.add(match_key)
                if len(matched_examples) < 10:
                    matched_examples.append(f"{jp_title} -> {match['source_file']}")
            else:
                missing_topics.append(jp_title)
                
    coverage = (matched_topics / total_topics) * 100 if total_topics > 0 else 0
    utilization = (len(used_keys) / len(lookup)) * 100 if lookup else 0
    
    print("-" * 50)
    print(f"Total Topics in New Data: {total_topics}")
    print(f"Matched Topics from Old Translations: {matched_topics}")
    print(f"Total Unique Old Translations: {len(lookup)}")
    print(f"Coverage of New Data: {coverage:.2f}%")
    print(f"Utilization of Old Translations: {utilization:.2f}%")
    print("-" * 50)

    print("\nSample Matched Topics:")
    for m in matched_examples:
        print(f" [MATCH] {m}")

    print("\nSample Missing Topics (New Data has, Old doesn't):")
    for t in missing_topics[:10]:
        print(f" [MISS] {t} (Cleaned: {clean_title(t)})")

    print("\nSample Unused Old Translations (Old has, New Data doesn't):")
    unused = [k for k in lookup.keys() if k not in used_keys]
    for u in unused[:10]:
        print(f" [UNUSED] {u}")

if __name__ == "__main__":
    print("Starting analysis...")
    lookup_table = load_old_translations()
    analyze_coverage_improved(lookup_table)
