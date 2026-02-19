
file_path = '/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/translated_parts/theme_03_浄化作用_part_07.json'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 10 is index 9
target_line = lines[9]
print(f"Line 10 length: {len(target_line)}")
print(f"Start: {target_line[:100]!r}")
print(f"End: {target_line[-50:]!r}")

# Check for unescaped quotes inside
content_str = target_line.strip()
if content_str.startswith('"content": "') and content_str.endswith('",'):
    inner = content_str[12:-2] # remove "content": " and ",
    # Count quotes
    # But wait, specific unescaped ones matter.
    # Let's just print surrounding chars of any quote
    for i, char in enumerate(inner):
        if char == '"' and (i == 0 or inner[i-1] != '\\'):
            print(f"Found unescaped quote at index {i}: ...{inner[max(0, i-10):min(len(inner), i+10)]}...")

print("Done checking.")
