import json
import os
import glob

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
ORIGINAL_JSON = os.path.join(BASE_DIR, "shumeic1_part2_data.json")
TRANSLATED_DIR = os.path.join(BASE_DIR, "translated_parts")

def main():
    with open(ORIGINAL_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    theme1 = data["themes"][1] # Theme 1
    orig_topics = theme1["topics"]
    
    # Load translated items
    translated_files = glob.glob(os.path.join(TRANSLATED_DIR, "theme_02_*.json"))
    translated_files.sort()
    
    translated_items = []
    for tf in translated_files:
        with open(tf, 'r', encoding='utf-8') as f:
            translated_items.extend(json.load(f))
            
    print(f"Total Original Topics: {len(orig_topics)}")
    print(f"Total Translated Items: {len(translated_items)}")
    
    start = 120
    end = 140
    
    print(f"\nComparing indices {start} to {end}:")
    print(f"{'Idx':<5} | {'Original Filename':<30} | {'Translated Source File':<30} | {'Match?'}")
    print("-" * 80)
    
    for i in range(start, end):
        orig_file = orig_topics[i]["filename"] if i < len(orig_topics) else "N/A"
        
        if i < len(translated_items):
            trans_file = translated_items[i].get("source_file", "N/A")
        else:
            trans_file = "N/A"
            
        match = "YES" if os.path.basename(orig_file) == os.path.basename(trans_file) else "NO"
        if match == "NO" and (orig_file == "N/A" or trans_file == "N/A"):
             match = "-"

        print(f"{i:<5} | {os.path.basename(orig_file):<30} | {os.path.basename(trans_file):<30} | {match}")

if __name__ == "__main__":
    main()
