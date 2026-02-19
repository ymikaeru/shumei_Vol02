import json

filepath = "Data/translated_parts/theme_03_霊主体従_part_02.json"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
inside_content = False
buffer = ""

for i, line in enumerate(lines):
    # This is a heuristic based on the viewed file content
    if i == 23: # Line 24
        buffer = line.rstrip('\n') # Keep indentation and start
        inside_content = True
        continue
    
    if inside_content:
        # If we reached the end of the block (Line 30 starts with "  },")
        if line.strip() == "},":
            # Append the buffer to new_lines, closing the quote if missing (it shouldn't be for this file based on view)
            # Actually line 29 ends with .
            # We need to process the buffer.
            # We join the lines with literal \n
            # But we need to check if the last line had the closing quote.
            pass
        elif i == 29: # The confirmed last line of the block
             # This line ends with .
             # We assume this is the end.
             # We add the line content.
             # We need to replace the newline at the start of THIS line if it matters, but we are joining.
             # The previous lines need to be joined with \n.
             buffer += r"\n" + line.strip()
             new_lines.append(buffer + "\n")
             inside_content = False
             continue
        else:
            # Intermediate lines (25, 26, 27, 28)
            # Remove indent?
            # Line 27 is . Line 28 is .
            # We should preserve the text but format as single line.
            # We replace actual newline with \n
            buffer += r"\n" + line.strip() 
            continue

    new_lines.append(line)

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Verify
try:
    with open(filepath, "r", encoding="utf-8") as f:
        json.load(f)
    print("JSON contains valid syntax now.")
except Exception as e:
    print(f"Still invalid: {e}")
