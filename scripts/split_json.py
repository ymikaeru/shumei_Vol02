import json
import os
import re

def slugify(text):
    # Basic slugify to make filenames safe
    text = text.replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', text)

def split_json(input_file, output_dir, chunk_size=15):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    volume_title = data.get('volume_title', 'Volume 2')
    themes = data.get('themes', [])

    for t_idx, theme in enumerate(themes):
        theme_title = theme.get('theme_title', f'Theme_{t_idx+1}')
        topics = theme.get('topics', [])
        
        # Split topics into chunks of chunk_size
        for p_idx in range(0, len(topics), chunk_size):
            chunk = topics[p_idx:p_idx + chunk_size]
            
            output_data = {
                "volume_title": volume_title,
                "theme_title": theme_title,
                "part": (p_idx // chunk_size) + 1,
                "total_parts": (len(topics) + chunk_size - 1) // chunk_size,
                "topics": chunk
            }
            
            safe_theme_title = slugify(theme_title)
            filename = f"theme_{t_idx+1:02d}_{safe_theme_title}_part_{output_data['part']:02d}.json"
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(output_data, out_f, ensure_ascii=False, indent=2)
            
            print(f"Generated: {filename} ({len(chunk)} topics)")

if __name__ == "__main__":
    INPUT_FILE = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/shumeic2_data.json"
    OUTPUT_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/parts_for_translation"
    split_json(INPUT_FILE, OUTPUT_DIR)
