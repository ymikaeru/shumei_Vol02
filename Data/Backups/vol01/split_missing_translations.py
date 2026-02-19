
import json
import os
import math

def split_json(input_file, output_dir, chunk_size=15):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_items = len(data)
    num_chunks = math.ceil(total_items / chunk_size)

    print(f"Splitting {total_items} items into {num_chunks} chunks of ~{chunk_size} items each.")

    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_items)
        chunk = data[start_idx:end_idx]

        output_filename = os.path.join(output_dir, f"missing_part_{i+1:02d}.json")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        
        print(f"Created {output_filename} with {len(chunk)} items.")

if __name__ == "__main__":
    input_file = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/missing_translations.json"
    output_dir = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/missing_parts_for_translation"
    split_json(input_file, output_dir)
