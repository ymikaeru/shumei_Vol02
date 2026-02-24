import json
import os
import glob

# Configuration
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
INPUT_JSON = os.path.join(BASE_DIR, "shumeic1_data.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "v1_parts_for_translation")

# Limits for splitting
MAX_TOPICS_PER_FILE = 20

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_topics(topics, max_count=MAX_TOPICS_PER_FILE):
    chunks = []
    current_chunk = []
    
    for topic in topics:
        if len(current_chunk) >= max_count:
            chunks.append(current_chunk)
            current_chunk = []
            
        current_chunk.append(topic)
        
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def main():
    ensure_dir(OUTPUT_DIR)
    
    if not os.path.exists(INPUT_JSON):
        print(f"Error: {INPUT_JSON} not found.")
        return

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get("themes", [])
    print(f"Found {len(themes)} themes to split.")

    for t_idx, theme in enumerate(themes):
        theme_title = theme.get("theme_title", "")
        # Clean title for filename mapping
        safe_title = theme_title.replace(" ", "_").replace("/", "_")
        topics = theme.get("topics", [])
        
        # Split topics
        topic_chunks = split_topics(topics, MAX_TOPICS_PER_FILE)
        
        print(f"Theme {t_idx+1:02d}: {theme_title} | Topics: {len(topics)} | Chunks: {len(topic_chunks)}")
        
        for i, chunk in enumerate(topic_chunks):
            part_data = {
                "theme_title": theme_title,
                "part_index": i + 1,
                "total_parts": len(topic_chunks),
                "topics": chunk
            }
            
            # Construct filename: theme_XX_Name_part_YY.json
            part_filename = f"theme_{t_idx+1:02d}_{safe_title}_part_{i+1:02d}.json"
            output_path = os.path.join(OUTPUT_DIR, part_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(part_data, f, ensure_ascii=False, indent=2)
                
    print(f"\nSplit complete. Files saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
