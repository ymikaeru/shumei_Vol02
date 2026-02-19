
import json
import sys

file_path = '/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data/translated_parts/theme_03_浄化作用_part_07.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try parsing
    data = json.loads(content)
    print("JSON is valid.")
    
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    print(f"Line: {e.lineno}")
    print(f"Col: {e.colno}")
    print(f"Msg: {e.msg}")
    
    # Print the context around the error
    lines = content.split('\n')
    error_line_idx = e.lineno - 1
    if 0 <= error_line_idx < len(lines):
        line = lines[error_line_idx]
        print(f"Content of line {e.lineno}:")
        # Print a snippet around the column
        start = max(0, e.colno - 50)
        end = min(len(line), e.colno + 50)
        print(f"...{line[start:end]}...")
        print(" " * (3 + (e.colno - start)) + "^")
