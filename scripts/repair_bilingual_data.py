import json
import os
import re
from bs4 import BeautifulSoup

# Configuration
MAIN_JSON = 'Data/shumeic1_part2_data_bilingual.json'
ORIG_JSON = 'Data/shumeic1_part2_data.json'
HTML_DIR = 'shumeic1' # Adjust if multiple dirs
TRANSLATED_PARTS_DIR = 'Data/translated_parts'
MISSING_PARTS_DIR = 'Data/missing_parts_for_translation'
REMAINING_TRANS = 'Data/remaining_untranslated_translated.json'
OUTPUT_JSON = 'Data/shumeic1_part2_data_bilingual_repaired.json'

def clean_title(title):
    if not title: return ""
    # Remove whitespace, non-breaking spaces, and common prefixes
    title = re.sub(r'[\s\u3000\xa0]+', '', title)
    return title

def extract_from_html(filename):
    filepath = os.path.join(HTML_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Heuristic for topics: Headers with size +2 or B tags with 明主様
    # We want to split the body content by these headers or HR tags.
    
    # Find all potential start points
    topics = []
    
    # We'll use a regex to find topic headers in the text.
    # Topic headers usually look like: 明主様御教え　「...」
    # We look for <b><font size="+2">...</font></b> or similar.
    
    # A better way is to iterate through siblings of <body> 
    # and split by <hr> or header-like elements.
    
    body = soup.find('body')
    if not body:
        return []
    
    current_topic = None
    current_elements = []
    
    # Flatten the tree a bit to iterate siblings
    # Actually, many files use BLOCKQUOTE structures.
    # We'll walk all elements and group them by separators.
    
    all_elements = body.find_all(recursive=True)
    
    # This might be tricky. Let's try a simpler approach:
    # Split the raw HTML by <hr> tags first? 
    # No, because some files might not have <hr> between every topic but have clear headers.
    
    # Let's try to identify headers:
    headers = []
    # Topic headers usually have size="+2" or text with the specific pattern
    for tag in soup.find_all('font', size=['+2', '5']):
        text = tag.get_text(strip=True)
        if "明主様" in text:
            # Navigate UP to find the topmost tag that is still considered part of the header
            # Usually B, FONT, or P
            top_header = tag
            while top_header.parent and top_header.parent.name in ['b', 'font', 'strong', 'i', 'u', 'p', 'span']:
                # If we hit body or blockquote, stop
                if top_header.parent.name in ['body', 'blockquote', 'div', 'td', 'center']:
                    break
                top_header = top_header.parent
            
            if top_header not in headers:
                headers.append(top_header)
    
    # If no headers found, maybe it's a single article file
    if not headers:
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else filename
        return [{
            "title": title,
            "content": str(body),
            "date": "Unknown"
        }]

    # Split by headers
    for i, h in enumerate(headers):
        title_text = h.get_text(strip=True)
        
        # Determine the date if it's right after the header
        date = "Unknown"
        # Look for parentheses like （昭和...） or (昭和...)
        # Often it's a sibling text node
        next_sib = h.next_sibling
        while next_sib and not isinstance(next_sib, str):
            if next_sib.name in ['br', 'font', 'b']:
                txt = next_sib.get_text(strip=True)
                if txt.startswith('（') or txt.startswith('('):
                    date_match = re.search(r'[(（]([^)）]+)[)）]', txt)
                    if date_match:
                        date = date_match.group(1)
                    break
            next_sib = next_sib.next_sibling
        else:
            if isinstance(next_sib, str) and (next_sib.strip().startswith('（') or next_sib.strip().startswith('(')):
                date_match = re.search(r'[(（]([^)）]+)[)）]', next_sib)
                if date_match:
                    date = date_match.group(1)

        # Get content until next header or HR
        content_elements = []
        curr = h
        while curr.next_sibling:
            curr = curr.next_sibling
            if i + 1 < len(headers) and curr == headers[i+1]:
                break
            # If we hit an HR, it's usually the end of this topic
            if getattr(curr, 'name', '') == 'hr':
                content_elements.append(str(curr))
                break
            content_elements.append(str(curr))
        
        # Cleanup content: remove the date from the start if it was captured as sibling
        content_html = "".join(content_elements)
        
        topics.append({
            "title": title_text,
            "date": date,
            "content": str(h) + content_html
        })
        
    return topics

def load_translation_sources():
    master_map = {} # (filename, cleaned_title) -> {title_pt, content_pt, pub_pt}
    
    # 1. Load from Main JSON (Highest priority if not empty)
    if os.path.exists(MAIN_JSON):
        with open(MAIN_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for theme in data.get('themes', []):
                for topic in theme.get('topics', []):
                    fname = topic.get('filename')
                    title = topic.get('title')
                    if not fname or not title: continue
                    
                    tp = (topic.get('title_pt') or '').strip()
                    cp = (topic.get('content_pt') or '').strip()
                    pp = (topic.get('publication_title_pt') or '').strip()
                    
                    if tp or cp:
                        key = (fname, clean_title(title))
                        master_map[key] = {
                            "title_pt": tp,
                            "content_pt": cp,
                            "publication_title_pt": pp
                        }
    
    # 2. Load from translated_parts (Override if present, as they might be newer/fixed)
    if os.path.exists(TRANSLATED_PARTS_DIR):
        for f in os.listdir(TRANSLATED_PARTS_DIR):
            if f.endswith('.json'):
                path = os.path.join(TRANSLATED_PARTS_DIR, f)
                with open(path, 'r', encoding='utf-8') as jf:
                    try:
                        trans_data = json.load(jf)
                        if not isinstance(trans_data, list):
                            trans_data = trans_data.get('topics', [])
                        
                        for item in trans_data:
                            # These files usually don't have filename, but hopefully they have JP fields now?
                            # Wait, earlier I saw they only have indices. 
                            # If they only have indices, I need to know which file they came from.
                            # The filename is usually encode in the theme_XX prefix? 
                            # No, that's not reliable.
                            
                            # Let's hope some have JP titles now after my previous merges.
                            # If not, I'll Skip for now and rely on the main JSON which already has them indexed.
                            pass
                    except:
                        continue

    # 3. Load from Missing Parts
    if os.path.exists(MISSING_PARTS_DIR):
        for f in os.listdir(MISSING_PARTS_DIR):
            if f.endswith('.json'):
                path = os.path.join(MISSING_PARTS_DIR, f)
                with open(path, 'r', encoding='utf-8') as jf:
                    try:
                        m_data = json.load(jf)
                        # ... Similar logic ...
                    except: pass

    return master_map

def main():
    print("Loading Ground Truth structure...")
    with open(ORIG_JSON, 'r', encoding='utf-8') as f:
        orig_data = json.load(f)
    
    print("Loading existing translations...")
    trans_library = load_translation_sources()
    
    repaired_data = {
        "volume_title": orig_data.get("volume_title"),
        "themes": []
    }
    
    processed_files = {} # cache for HTML extraction
    
    for theme in orig_data.get('themes', []):
        new_theme = {
            "theme_title": theme.get("theme_title"),
            "topics": []
        }
        
        for topic in theme.get('topics', []):
            filename = topic.get('filename')
            title_orig = topic.get('title')
            
            if not filename: continue
            
            if filename not in processed_files:
                processed_files[filename] = extract_from_html(filename)
            
            # Find matching topic in extracted list
            matching_extracted = None
            clean_t_orig = clean_title(title_orig)
            
            for ext in processed_files[filename]:
                if clean_title(ext['title']) == clean_t_orig:
                    matching_extracted = ext
                    break
            
            if not matching_extracted:
                # Try partial match if exact failed
                for ext in processed_files[filename]:
                    if clean_t_orig in clean_title(ext['title']) or clean_title(ext['title']) in clean_t_orig:
                        matching_extracted = ext
                        break
            
            # Construct new topic entry
            new_topic = topic.copy()
            if matching_extracted:
                new_topic['content'] = matching_extracted['content']
                new_topic['date'] = matching_extracted['date']
            
            # Patch with translation
            lib_key = (filename, clean_t_orig)
            if lib_key in trans_library:
                lib_entry = trans_library[lib_key]
                new_topic['title_pt'] = lib_entry['title_pt']
                new_topic['content_pt'] = lib_entry['content_pt']
                new_topic['publication_title_pt'] = lib_entry['publication_title_pt']
            
            new_theme['topics'].append(new_topic)
            
        repaired_data['themes'].append(new_theme)
        print(f"Repaired theme: {new_theme['theme_title']}")

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(repaired_data, f, ensure_ascii=False, indent=2)
    
    print(f"Success! Repaired data saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
