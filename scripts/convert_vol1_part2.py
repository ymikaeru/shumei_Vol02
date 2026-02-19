import os
import json
import re
from bs4 import BeautifulSoup

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/shumeic1"
DATA_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
INDEX_FILE = os.path.join(BASE_DIR, "index2.html")
OUTPUT_FILE = os.path.join(DATA_DIR, "shumeic1_part2_data.json")

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def extract_date_from_text(text):
    # Pattern to find date in format （昭和23年2月28日） or similar
    match = re.search(r'（(.*?)）', text)
    if match:
        return match.group(1)
    return None

def parse_linked_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp932') as f:
                content = f.read()
        except:
            print(f"Failed to read file with utf-8 or cp932: {file_path}")
            return []

    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove navigation links first to clean up content
    if soup.body:
        for nav in soup.find_all('a', href=True):
            if nav['href'] in ['index.html', 'index2.html', '#']:
                nav.decompose()
        # Also remove the "top" buttons often found at bottom
        for img in soup.find_all('img'):
            if 'btn' in str(img.get('src', '')):
                if img.parent and img.parent.name == 'a':
                     img.parent.decompose()
                else:
                     img.decompose()

    # Find all potential topic headers
    # Heuristic: <font size="+2"> usually marks the title
    font_tags = soup.find_all('font', size='+2')
    
    # Filter to likely titles (usually inside bold or just text, excluding the main file title if repeated)
    # In keirin2.html, the main title is at top, then sub-topics follow.
    # Actually, we can just treat ALL <font size="+2"> as potential start of a new section 
    # IF they are followed by content or a date.
    
    # However, sometimes the very first one is just the Page Title, and the first actual topic starts immediately or later.
    # In keirin2.html:
    # 1. 　　神と経綸について　２ (Page Page)
    # 2. 明主様御講義　「宗教の根源と救世主の出現」 (Topic 1)
    # 3. 明主様御講義　「悪の経綸」 (Topic 2)
    # ...
    
    # We need to distinguish "Page Title" from "Topic Title".
    # Page Title often matches the link text from index.
    
    topics = []
    
    # If no font tags, treat whole file as one topic
    if not font_tags:
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)
            
        # Try to find date in whole content
        date = "Unknown"
        paren_pattern = re.compile(r'（(.*?)）')
        date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')
        
        paren_matches = paren_pattern.findall(content) # Use raw content for date search if needed? No, use soup text
        # Better to search in soup text to avoid script tags etc? 
        # For date, raw content is finer as long as we don't pick up metadata.
        
        match = date_validator.search(soup.get_text()) # Simple search in text
        if match:
             date = match.group(0) # Use group 0 for full match including Japanese era
        
        # Get content
        body_content = ""
        main_blockquote = soup.find('blockquote')
        if main_blockquote:
            body_content = str(main_blockquote)
        else:
            body_content = str(soup.body) if soup.body else str(soup)
            
        return [{'title': title, 'date': date, 'content': body_content}]

    # We have font tags. Let's see if we can split content.
    # Strategy: 
    # 1. Identify valid headers.
    # 2. Split soup content based on these headers.
    
    # Regex for date extraction
    paren_pattern = re.compile(r'（(.*?)）')
    date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')

    valid_headers = []
    for ft in font_tags:
        text = ft.get_text(strip=True)
        if not text:
            continue
            
        # Check if it has a date near it
        # Siblings check
        has_date = False
        date_str = "Unknown"
        
        check_text = ""
        if ft.next_sibling:
             check_text += str(ft.next_sibling)
        if ft.parent:
             check_text += ft.parent.get_text()
             if ft.parent.next_sibling:
                 check_text += str(ft.parent.next_sibling)
        
        # Extract date
        paren_matches = paren_pattern.findall(check_text)
        for p_content in paren_matches:
            d_match = date_validator.search(p_content)
            if d_match:
                date_str = d_match.group(1)
                has_date = True
                break
        
        # If no date found but looks like a proper title (e.g. starts with 明主様 or specific keywords), we may still accept it
        if not has_date:
            if "明主様" in text or "御教え" in text or "御講義" in text:
                 pass # Very likely a title
            else:
                 # Might be just the page title or decoration
                 # If it is the VERY first one, it might be the page title. 
                 # But if we have multiple "topics", the page title might be distinct.
                 # Let's collect it anyway, and maybe merge if it looks like a duplicate.
                 pass

        valid_headers.append({
            'node': ft,
            'title': text,
            'date': date_str
        })

    # Filter out nested headers (e.g. <font><font>Title</font></font>)
    # If a header node is a descendant of another header node, keep only the outer one (or the one that seems to be the parent).
    # Actually, we rely on the list being in document order.
    # If A contains B, A comes first? valid_headers preserves find_all order (document order).
    # If A contains B, A is found first.
    final_headers = []
    for h in valid_headers:
        is_nested = False
        for existing in final_headers:
            # Check if h['node'] is a descendant of existing['node']
            if existing['node'] in h['node'].parents:
                is_nested = True
                break
        if not is_nested:
            final_headers.append(h)
    
    valid_headers = final_headers

    # If only 1 valid header found, return as single topic
    # If multiple found, we need to split.
    
    # Refined logic: If the first header looks like "Page Title" (e.g. matches filename concept or just "Theme Name"), 
    # and there are subsequent headers that look like "Topic Titles", ignore the first one as a split point?
    # For now, let's treat all valid headers as split points.
    
    if not valid_headers:
         # Fallback similar to no font tags
         body_content = str(soup.body) if soup.body else str(soup)
         return [{'title': "No Title", 'date': "Unknown", 'content': body_content}]

    # Splitting logic
    # We iterate through siblings of the headers to build content for each. 
    # This is tricky because headers might be nested or at different levels.
    # BUT, looking at the HTML, they seem to be usually at similar levels or inside Blockquotes.
    
    # Simplified approach: Use string splitting on the raw HTML if possible? 
    # No, risky.
    # Better: Identify the start node of each section. Collect all siblings until next start node.
    
    # Let's try to map nodes to their linear position or just process visually.
    # Another approach: iterate over all Blockquote contents? 
    
    # Let's rely on the fact that `font size=+2` marks the start.
    # We will reconstruct content for each section.
    
    processed_topics = []
    
    # If the first header seems to be a main title (no date, generic name) and there are others with dates/specific names,
    # skip the first one for topic creation but maybe keep it as context?
    # User example: "神と経綸について　２" is the file title. 
    # "明主様御講義..." are the topics.
    
    start_index = 0
    if len(valid_headers) > 1:
        # Check first header
        first = valid_headers[0]
        # Heuristic: if first title is short/generic and Date is Unknown, and 2nd has Date or detailed title
        if first['date'] == "Unknown" and len(valid_headers) > 1:
             start_index = 1
        
        if "kanzeon2" in file_path:
             print(f"DEBUG: kanzeon2 - First Header Date: '{first['date']}'")
             print(f"DEBUG: kanzeon2 - Start Index: {start_index}")
             print(f"DEBUG: kanzeon2 - Valid Headers Count: {len(valid_headers)}")
    
    # If we decided to skip the first header, it means the FIRST topic actually starts at the 2nd header.
    # The content BEFORE the 2nd header is arguably "Page Preamble" or belongs to the skipped header.
    # In JSON structure, we only want the topics.
    
    for i in range(start_index, len(valid_headers)):
        current_header = valid_headers[i]
        header_node = current_header['node']
        
        # Determine end boundary
        # It's the next valid header, or end of doc
        next_header_node = valid_headers[i+1]['node'] if (i + 1) < len(valid_headers) else None
        
        # Extract content
        # We need to capture the HTML between header_node and next_header_node.
        # This is where BeautifulSoup is messy. 
        # Hacky but effective way for this specific legacy HTML:
        # 1. Find the parent block of the header (usually it's inside <Blockquote> or <p>)
        # The structure is often flat text mixed with tags. 
        
        # Let's try to grab everything following the header node until the next header node.
        # But we need to handle hierarchy. 
        
        # Alternative: markers.
        # Insert unique markers into the soup before each header.
        # `###SPLIT_MARKER_i###`
        # Then get str(soup), split by markers.
        pass

    # Marker insertion strategy
    for idx, item in enumerate(valid_headers):
        marker = soup.new_tag('div')
        marker.string = f"###SPLIT_MARKER_{idx}###"
        # Insert before the font tag. 
        # If font tag is inside B, insert before B?
        target = item['node']
        if target.parent and target.parent.name == 'b':
            target = target.parent
        if target.parent and target.parent.name == 'u':
            target = target.parent
            
        target.insert_before(marker)
        
    # Now convert to string and split
    # We need to limit scope to the main container if possible to avoid <head> etc.
    # Usually <body> or main <blockquote>
    
    # If we assume the headers are inside the body/blockquote
    full_html = str(soup.body) if soup.body else str(soup)
    
    parts = re.split(r'<div>###SPLIT_MARKER_\d+###</div>|&lt;div&gt;###SPLIT_MARKER_\d+###&lt;/div&gt;', full_html)
    
    # parts[0] is content before first header.
    # parts[1] is content of header 0
    # parts[2] is content of header 1 ...
    
    # If we skipped index 0 in our loop above, we should align logic.
    # valid_headers[k] corresponds to parts[k+1] usually.
    
    # Let's map back
    final_topics = []
    
    # Check alignment
    # If we inserted N markers, we should have N+1 parts.
    # Part 0: pre-content
    # Part 1: content for Header 0
    # ...
    
    for i in range(len(valid_headers)):
        # We check our start_index logic again.
        if i < start_index:
            continue
            
        h_info = valid_headers[i]
        
        # Content is in parts[i+1]
        if (i+1) < len(parts):
            raw_content = parts[i+1]
            # Clean up content?
            # Ideally wrap in a div or something if it's fragments?
            # The User wants "Content".
            
            # Remove the header title itself from the content if extracted?
            # Usually the user keeps the header in the content too, or removes it.
            # In the previous logic, we kept everything. 
            # But since we extracted Title separatey, maybe good to remove the specific title string from content to avoid duplication?
            # Or just keep it as is. Let's keep it to be safe (preserve original formatting).
            
            # Wait, the marker was inserted BEFORE the header. So the header IS included in the part.
            
            # Check if content has body text
            # parts[i+1] contains the header and the content following it.
            # We want to ensure there is actual content involved.
            content_soup = BeautifulSoup(raw_content, 'html.parser')
            body_text = clean_text(content_soup.get_text())
            title_text = clean_text(h_info['title'])
            
            # Logic: If the text content is roughly just the title, then it's an empty section header.
            # We remove the title from the body text.
            # Be careful with partial matches, but usually title is at the start.
            
            remainder = body_text.replace(title_text, '', 1).strip() # Replace only first occurrence
            
            if h_info['date'] != "Unknown":
                 remainder = remainder.replace(h_info['date'], '', 1).strip()
            
            # Threshold for "significant content"
            # Some topics might be just an image? 
            # If there are img tags, we should keep it.
            has_img = bool(content_soup.find('img'))

            if len(remainder) < 5 and not has_img:
                 # print(f"Skipping empty topic: {h_info['title']}")
                 continue

            final_topics.append({
                'title': h_info['title'],
                'date': h_info['date'],
                'content': raw_content.strip()
            })
            
    return final_topics

def main():
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(INDEX_FILE, 'r', encoding='cp932') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    themes = []
    
    # 1. Find all blue font tags (Theme Headers)
    # The structure seems to be flat within a blockquote for most parts
    theme_headers = soup.find_all('font', color='#0000ff')
    
    for header in theme_headers:
        theme_name = clean_text(header.get_text())
        
        # Skip top level title if it matches vaguely
        if "通信カレッジ" in theme_name or not theme_name:
            continue
            
        print(f"Processing Theme: {theme_name}")
        
        topics = []
        
        # Traverse siblings
        next_node = header.next_sibling
        
        while next_node:
            # Stop if we hit the next theme header
            if next_node.name == 'font' and next_node.get('color') == '#0000ff':
                break
            
            # Stop if we hit a horizontal rule
            if next_node.name == 'hr':
                break
            
            # If it's a link directly
            if next_node.name == 'a':
                href = next_node.get('href')
                link_text = clean_text(next_node.get_text())
                if href and href not in ['index.html', 'index2.html', '#']:
                    # Process file
                    file_path = os.path.join(BASE_DIR, href)
                    file_topics = parse_linked_file(file_path)
                    
                    if not file_topics:
                        continue
                        
                    for t in file_topics:
                        if not t['title']:
                            t['title'] = link_text
                        
                        t['filename'] = href
                        topics.append(t)

            # If it's a font tag (likely containing links)
            elif next_node.name == 'font':
                for a in next_node.find_all('a'):
                    href = a.get('href')
                    link_text = clean_text(a.get_text())
                    if href and href not in ['index.html', 'index2.html', '#']:
                        # Process file
                        file_path = os.path.join(BASE_DIR, href)
                        file_topics = parse_linked_file(file_path)
                        
                        if not file_topics:
                             # Fallback or empty?
                             continue
                             
                        for t in file_topics:
                            if not t['title']:
                                t['title'] = link_text
                            
                            t['filename'] = href
                            topics.append(t)
            
            next_node = next_node.next_sibling

        if theme_name:
            themes.append({
                "theme_title": theme_name,
                "topics": topics
            })

    output_data = {
        "volume_title": "経綸・霊主体従・夜昼転換・祖霊祭祀編",
        "themes": themes
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved JSON to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
