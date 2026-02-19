
import json
import os
import math

def consolidate_parts():
    input_file = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/missing_translations.json"
    output_dir = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/missing_parts_for_translation"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    # Part 1 is already done (15 items)
    # We want to re-split items from index 15 to the end
    start_index = 15
    remaining_data = all_data[start_index:]
    total_remaining = len(remaining_data)
    
    # Target: 3 files for the remaining 99 items -> 33 items per file
    chunk_size = 33
    num_chunks = math.ceil(total_remaining / chunk_size)
    
    print(f"Consolidating {total_remaining} items into {num_chunks} chunks of ~{chunk_size} items each.")

    for i in range(num_chunks):
        chunk_start = i * chunk_size
        chunk_end = min((i + 1) * chunk_size, total_remaining)
        chunk = remaining_data[chunk_start:chunk_end]
        
        # File indices start at 02 because 01 is preserved
        file_index = i + 2
        output_filename = os.path.join(output_dir, f"missing_part_{file_index:02d}.json")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        
        print(f"Created {output_filename} with {len(chunk)} items.")

    # Delete excess files if they exist (05 to 08)
    # We expect to create 02, 03, 04. So anything from 05 upwards should be removed.
    existing_files = sorted([f for f in os.listdir(output_dir) if f.startswith("missing_part_") and f.endswith(".json")])
    
    # We want to keep 01, 02, 03, 04
    files_to_keep = {f"missing_part_{i:02d}.json" for i in range(1, file_index + 1)}
    
    for filename in existing_files:
        if filename not in files_to_keep:
            file_path = os.path.join(output_dir, filename)
            os.remove(file_path)
            print(f"Deleted excess file: {filename}")

if __name__ == "__main__":
    consolidate_parts()
