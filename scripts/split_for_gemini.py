import json
import os
import glob

# Configuration
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
INPUT_DIR = os.path.join(BASE_DIR, "parts_for_translation")
OUTPUT_DIR = os.path.join(BASE_DIR, "parts_for_translation_granular")

# New target: 10 topics per file to ensure Gemini can translate the whole content in one response.
MAX_TOPICS_PER_FILE = 10

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    ensure_dir(OUTPUT_DIR)
    
    json_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.json")))
    
    if not json_files:
        print(f"No JSON files found in {INPUT_DIR}")
        return

    print(f"Processing {len(json_files)} files...")
    
    total_new_files = 0
    for file_path in json_files:
        filename = os.path.basename(file_path)
        base_name, _ = os.path.splitext(filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        theme_title = data.get("theme_title", "")
        volume_title = data.get("volume_title", "")
        topics = data.get("topics", [])
        
        # Split topics into chunks of MAX_TOPICS_PER_FILE
        chunks = [topics[i:i + MAX_TOPICS_PER_FILE] for i in range(0, len(topics), MAX_TOPICS_PER_FILE)]
        
        for i, chunk in enumerate(chunks):
            part_data = {
                "volume_title": volume_title,
                "theme_title": theme_title,
                "part_index": i + 1,
                "total_parts_of_this_set": len(chunks),
                "topics": chunk
            }
            
            # Construct filename: theme_XX_Name_part_XX_sub_XX.json
            new_filename = f"{base_name}_sub_{i+1:02d}.json"
            output_path = os.path.join(OUTPUT_DIR, new_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(part_data, f, ensure_ascii=False, indent=2)
            
            total_new_files += 1

    print(f"\nGranular split complete.")
    print(f"Original files: {len(json_files)}")
    print(f"New granular files: {total_new_files}")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
