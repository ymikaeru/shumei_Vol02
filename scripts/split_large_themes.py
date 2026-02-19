import json
import os
import glob
import math

# Configuration
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
INPUT_DIR = os.path.join(BASE_DIR, "split_parts")
OUTPUT_DIR = os.path.join(BASE_DIR, "split_parts_granular")

# Limits for splitting
MAX_TOPICS_PER_FILE = 20
MAX_SIZE_BYTES = 50 * 1024  # Approx 50KB

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_topics(topics, max_count=MAX_TOPICS_PER_FILE, max_size=MAX_SIZE_BYTES):
    """
    Splits a list of topics into chunks based on count and estimated size.
    For simplicity, we primarily use count, but we could add size checks.
    Given the typical size of text, 15-20 topics is a reasonable safe limit for context windows.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    
    for topic in topics:
        topic_size = len(json.dumps(topic, ensure_ascii=False).encode('utf-8'))
        
        # Check if adding this topic exceeds limits
        if (len(current_chunk) >= max_count) or \
           (current_size + topic_size > max_size and current_chunk):

            
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
            
        current_chunk.append(topic)
        current_size += topic_size
        
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def main():
    ensure_dir(OUTPUT_DIR)
    
    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {INPUT_DIR}")
        return

    print(f"Found {len(json_files)} files to process.")
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        base_name, ext = os.path.splitext(filename)
        
        # Determine limits based on theme
        # Default limits
        limit_topics = MAX_TOPICS_PER_FILE
        limit_size = MAX_SIZE_BYTES
        
        # Theme 9 special limits (Requested by user: max safe tokens for Gemini)
        # Increasing to ~80KB and 40 topics to allow for larger chunks while keeping 
        # output generation (translation) likely within typical limits (or manageable with one continue).
        if "theme_09" in filename or "Theme_09" in filename:
             limit_topics = 40
             limit_size = 80 * 1024  # 80KB
             print(f"  Applying custom limits for Theme 9: {limit_topics} topics / {limit_size} bytes")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        theme_title = data.get("theme_title", "")
        topics = data.get("topics", [])
        
        # Split topics
        topic_chunks = split_topics(topics, limit_topics, limit_size)

        
        print(f"File: {filename} | Topics: {len(topics)} | Chunks: {len(topic_chunks)}")
        
        for i, chunk in enumerate(topic_chunks):
            # Create a simplified structure for the part
            part_data = {
                "theme_title": theme_title,
                "part_index": i + 1,
                "total_parts": len(topic_chunks),
                "topics": chunk
            }
            
            # If it's the first part, include volume title if available
            if i == 0 and "volume_title" in data:
                part_data["volume_title"] = data["volume_title"]
                
            # Construct filename: theme_XX_Name_part_01.json
            # We assume base_name is already theme_XX_Name
            part_filename = f"{base_name}_part_{i+1:02d}{ext}"
            output_path = os.path.join(OUTPUT_DIR, part_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(part_data, f, ensure_ascii=False, indent=2)
                
    print(f"\nGranular split complete. Files saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
