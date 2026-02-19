
import json

file_path = '/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/translated_parts/theme_03_浄化作用_part_07.json'
output_path = '/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/translated_parts/theme_03_浄化作用_part_07_fixed.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Regenerated JSON with ensure_ascii=False")
