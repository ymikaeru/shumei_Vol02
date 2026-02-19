import json

file_path = '/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/missing_parts_for_translation/missing_part_02.json'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

def find_invalid_escape(text):
    i = 0
    while i < len(text):
        if text[i] == '\\':
            if i + 1 >= len(text):
                print(f"Error: Backslash at end of file")
                return
            
            char = text[i+1]
            if char in '"\\/bfnrt':
                i += 2
                continue
            elif char == 'u':
                # Check next 4 chars are hex
                if i + 5 < len(text) and all(c in '0123456789abcdefABCDEF' for c in text[i+2:i+6]):
                    i += 6
                    continue
                else:
                     print(f"Error: Invalid unicode escape at index {i}")
                     line_num = text[:i].count('\n') + 1
                     print(f"Line: {line_num}")
                     print(f"Context: {text[i-10:i+20]}")
                     i += 2
            else:
                print(f"Error: Invalid escape \\{char} at index {i}")
                line_num = text[:i].count('\n') + 1
                print(f"Line: {line_num}")
                print(f"Context: {text[i-10:i+20]}")
                i += 2
        else:
            char = text[i]
            if ord(char) < 32:
                print(f"Error: Unescaped control character \\x{ord(char):02x} at index {i}")
                line_num = text[:i].count('\n') + 1
                print(f"Line: {line_num}")
                print(f"Context: {text[i-10:i+10]}")
            i += 1
            
find_invalid_escape(text)
print("Finished checking.")
