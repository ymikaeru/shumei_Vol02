import os
import json
import re
from bs4 import BeautifulSoup

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/shumeic2"
DATA_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
OUTPUT_FILE = os.path.join(DATA_DIR, "shumeic2_data.json")

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
    
    topics = []
    
    # If no font tags, treat whole file as one topic
    if not font_tags:
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)
            
        # Try to find date in whole content
        date = "Unknown"
        date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')
        
        match = date_validator.search(soup.get_text())
        if match:
             date = match.group(0)
        
        # Get content
        body_content = ""
        main_blockquote = soup.find('blockquote')
        if main_blockquote:
            body_content = str(main_blockquote)
        else:
            body_content = str(soup.body) if soup.body else str(soup)
            
        return [{'title': title, 'date': date, 'content': body_content}]

    # We have font tags. Let's see if we can split content.
    # Regex for date extraction
    paren_pattern = re.compile(r'（(.*?)）')
    date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')

    valid_headers = []
    for ft in font_tags:
        text = ft.get_text(strip=True)
        if not text:
            continue
            
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
        
        if not has_date:
            if "明主様" in text or "御教え" in text or "御講義" in text:
                 pass
            else:
                 pass

        valid_headers.append({
            'node': ft,
            'title': text,
            'date': date_str
        })

    final_headers = []
    for h in valid_headers:
        is_nested = False
        for existing in final_headers:
            if existing['node'] in h['node'].parents:
                is_nested = True
                break
        if not is_nested:
            final_headers.append(h)
    
    valid_headers = final_headers

    if not valid_headers:
         body_content = str(soup.body) if soup.body else str(soup)
         return [{'title': "No Title", 'date': "Unknown", 'content': body_content}]

    # Marker insertion strategy
    for idx, item in enumerate(valid_headers):
        marker = soup.new_tag('div')
        marker.string = f"###SPLIT_MARKER_{idx}###"
        target = item['node']
        if target.parent and target.parent.name == 'b':
            target = target.parent
        if target.parent and target.parent.name == 'u':
            target = target.parent
            
        target.insert_before(marker)
        
    full_html = str(soup.body) if soup.body else str(soup)
    parts = re.split(r'<div>###SPLIT_MARKER_\d+###</div>|&lt;div&gt;###SPLIT_MARKER_\d+###&lt;/div&gt;', full_html)
    
    final_topics = []
    start_index = 0
    if len(valid_headers) > 1:
        first = valid_headers[0]
        if first['date'] == "Unknown":
             # Check if first header is just a repeat of a title or a generic header
             start_index = 1

    for i in range(len(valid_headers)):
        if i < start_index:
            continue
            
        h_info = valid_headers[i]
        if (i+1) < len(parts):
            raw_content = parts[i+1]
            content_soup = BeautifulSoup(raw_content, 'html.parser')
            body_text = clean_text(content_soup.get_text())
            title_text = clean_text(h_info['title'])
            
            remainder = body_text.replace(title_text, '', 1).strip()
            if h_info['date'] != "Unknown":
                 remainder = remainder.replace(h_info['date'], '', 1).strip()
            
            has_img = bool(content_soup.find('img'))
            if len(remainder) < 5 and not has_img:
                 continue

            final_topics.append({
                'title': h_info['title'],
                'date': h_info['date'],
                'content': raw_content.strip()
            })
            
    return final_topics

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(INDEX_FILE, 'r', encoding='cp932') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    themes = []
    
    # Volume 2 uses <font color="#0000ff" face="メイリオ"> for themes
    theme_headers = soup.find_all('font', color='#0000ff')
    
    for header in theme_headers:
        theme_name = clean_text(header.get_text())
        
        # Skip top level title
        if "通信カレッジ" in theme_name and "浄霊" in theme_name:
            continue
        if not theme_name:
            continue
            
        print(f"Processing Theme: {theme_name}")
        topics = []
        
        # Traverse siblings
        next_node = header.next_sibling
        
        while next_node:
            if getattr(next_node, 'name', None) == 'font' and next_node.get('color') == '#0000ff':
                break
            
            if getattr(next_node, 'name', None) == 'hr':
                break
            
            if getattr(next_node, 'name', None) == 'a':
                href = next_node.get('href')
                link_text = clean_text(next_node.get_text())
                if href and href not in ['index.html', 'index2.html', '#'] and href.endswith('.html'):
                    file_path = os.path.join(BASE_DIR, href)
                    file_topics = parse_linked_file(file_path)
                    
                    if file_topics:
                        for t in file_topics:
                            if not t['title']:
                                t['title'] = link_text
                            t['filename'] = href
                            topics.append(t)

            elif getattr(next_node, 'name', None) == 'font' or getattr(next_node, 'name', None) == 'blockquote':
                # Recursively check for links in font or blockquote tags
                for a in next_node.find_all('a'):
                    href = a.get('href')
                    link_text = clean_text(a.get_text())
                    if href and href not in ['index.html', 'index2.html', '#'] and href.endswith('.html'):
                        file_path = os.path.join(BASE_DIR, href)
                        file_topics = parse_linked_file(file_path)
                        
                        if file_topics:
                            for t in file_topics:
                                if not t['title']:
                                    t['title'] = link_text
                                t['filename'] = href
                                topics.append(t)
            
            next_node = next_node.next_sibling

        if theme_name and topics:
            themes.append({
                "theme_title": theme_name,
                "topics": topics
            })

    output_data = {
        "volume_title": "浄霊・神示の健康法・自然農法編",
        "themes": themes
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved JSON to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
