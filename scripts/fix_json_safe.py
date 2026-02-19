import json

filepath = "Data/translated_parts/theme_03_霊主体従_part_02.json"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = 23
end_idx = 28 # inclusive

print(f"Replacing lines {start_idx+1} to {end_idx+1}:")
for i in range(start_idx, end_idx + 1):
    print(f"{i+1}: {lines[i].rstrip()}")

merged_line = lines[start_idx].rstrip('\n') 
for i in range(start_idx + 1, end_idx + 1):
    # Only adding \n if the previous line wasn't empty or trailing?
    # Simply joining with \n is safest to preserve structure.
    merged_line += r"\n" + lines[i].strip()

merged_line += '\n'

print("-" * 20)
print("Merged line preview (first 100 chars):")
print(merged_line[:100])
print("-" * 20)

new_lines = lines[:start_idx] + [merged_line] + lines[end_idx+1:]

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

try:
    with open(filepath, "r", encoding="utf-8") as f:
        json.load(f)
    print("SUCCESS: JSON is valid.")
except Exception as e:
    print(f"ERROR: JSON is still invalid: {e}")
