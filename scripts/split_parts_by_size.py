
import json
import os
import glob

# Configuration
PARTS_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/parts_for_translation"
MAX_CHARS_PER_FILE = 6000 # Soft limit for characters per file
THEMES_TO_PROCESS = ["theme_04", "theme_05", "theme_06", "theme_07", "theme_08", "theme_09"]

def get_file_size_estimate(data):
    """Estimate the size of the JSON data as a string."""
    return len(json.dumps(data, ensure_ascii=False))

def split_file(file_path):
    """Splits a JSON file into smaller chunks based on character count."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    topics = data.get("topics", [])
    if not topics:
        print(f"Skipping {file_path}: No topics found.")
        return

    base_name = os.path.basename(file_path)
    print(f"Processing {base_name} ({len(topics)} topics)...")

    # Group topics into chunks
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    # Base structure for new files (excluding topics)
    base_structure = {k: v for k, v in data.items() if k != "topics"}

    for topic in topics:
        topic_size = get_file_size_estimate(topic)
        
        # If adding this topic exceeds the limit AND we already have content, start a new chunk
        if current_chunk and (current_chunk_size + topic_size > MAX_CHARS_PER_FILE):
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_size = 0
        
        current_chunk.append(topic)
        current_chunk_size += topic_size

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    if len(chunks) <= 1:
        print(f"  - No split needed for {base_name} (Size: {get_file_size_estimate(data)} chars)")
        return

    print(f"  - Splitting {base_name} into {len(chunks)} files.")

    # Create new files
    original_filename_no_ext = os.path.splitext(base_name)[0]
    
    for i, chunk in enumerate(chunks):
        new_data = base_structure.copy()
        new_data["topics"] = chunk
        # Adjust part number info if needed, or leave as is since user just wants smaller files for translation
        # We will append _s{i+1} to the filename
        
        suffix = f"_s{i+1:02d}"
        new_filename = f"{original_filename_no_ext}{suffix}.json"
        new_file_path = os.path.join(PARTS_DIR, new_filename)
        
        try:
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            print(f"    Created: {new_filename} ({len(chunk)} topics, ~{get_file_size_estimate(new_data)} chars)")
        except Exception as e:
            print(f"    Error writing {new_filename}: {e}")

    # Move original file to backups
    BACKUPS_DIR = os.path.join(os.path.dirname(PARTS_DIR), "Backups")
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR)
        
    backup_path = os.path.join(BACKUPS_DIR, base_name + ".bak")
    try:
        os.rename(file_path, backup_path)
        print(f"    Moved original to {os.path.basename(backup_path)}")
    except Exception as e:
        print(f"    Error moving original: {e}")

def main():
    print(f"Scanning {PARTS_DIR}...")
    
    files = sorted(glob.glob(os.path.join(PARTS_DIR, "*.json")))
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Filter by theme
        is_target_theme = False
        for theme_prefix in THEMES_TO_PROCESS:
            if filename.startswith(theme_prefix):
                is_target_theme = True
                break
        
        if not is_target_theme:
            continue
            
        # Skip files that look like they are already split (contain _s01, etc) to avoid re-splitting
        # Regex or simple check
        if "_s0" in filename or "_s1" in filename: # Simple check for _s01, _s10 etc
            continue

        split_file(file_path)

    print("Done.")

if __name__ == "__main__":
    main()
