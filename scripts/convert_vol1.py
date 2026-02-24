import os
import json
import re
from bs4 import BeautifulSoup

# Paths for Volume 1
BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/OrigianlHTML/shumeic1"
DATA_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol02/Data"
INDEX_FILE = os.path.join(BASE_DIR, "index2.html")
OUTPUT_FILE = os.path.join(DATA_DIR, "shumeic1_data.json")

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

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
            print(f"Failed to read file: {file_path}")
            return []

    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove navigation
    if soup.body:
        for nav in soup.find_all('a', href=True):
            if nav['href'] in ['index.html', 'index2.html', '#']:
                nav.decompose()
        for img in soup.find_all('img'):
            if 'btn' in str(img.get('src', '')):
                if img.parent and img.parent.name == 'a':
                     img.parent.decompose()
                else:
                     img.decompose()

    font_tags = soup.find_all('font', size='+2')
    topics = []
    
    if not font_tags:
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)
            
        date = "Unknown"
        date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')
        match = date_validator.search(soup.get_text())
        if match:
             date = match.group(0)
        
        main_blockquote = soup.find('blockquote')
        body_content = str(main_blockquote) if main_blockquote else (str(soup.body) if soup.body else str(soup))
            
        return [{'title': title, 'date': date, 'content': body_content}]

    paren_pattern = re.compile(r'（(.*?)）')
    date_validator = re.compile(r'((?:昭和|大正|明治|平成)?\d+年(?:\d+月(?:\d+日)?)?)')

    valid_headers = []
    for ft in font_tags:
        text = ft.get_text(strip=True)
        if not text:
            continue
            
        date_str = "Unknown"
        check_text = ""
        if ft.next_sibling:
             check_text += str(ft.next_sibling)
        if ft.parent:
             check_text += ft.parent.get_text()
             if ft.parent.next_sibling:
                 check_text += str(ft.parent.next_sibling)
        
        paren_matches = paren_pattern.findall(check_text)
        for p_content in paren_matches:
            d_match = date_validator.search(p_content)
            if d_match:
                date_str = d_match.group(1)
                break

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
    
    start_index = 0
    if len(valid_headers) > 1:
        first = valid_headers[0]
        if first['date'] == "Unknown":
             start_index = 1
             
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
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(INDEX_FILE, 'r', encoding='cp932') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    themes = []
    theme_headers = soup.find_all('font', color='#0000ff')
    
    for header in theme_headers:
        theme_name = clean_text(header.get_text())
        if "通信カレッジ" in theme_name or not theme_name:
            continue
            
        print(f"Processing Theme: {theme_name}")
        topics = []
        next_node = header.next_sibling
        
        while next_node:
            if next_node.name == 'font' and next_node.get('color') == '#0000ff':
                break
            if next_node.name == 'hr':
                break
            
            if next_node.name == 'a':
                href = next_node.get('href')
                link_text = clean_text(next_node.get_text())
                if href and href not in ['index.html', 'index2.html', '#']:
                    file_topics = parse_linked_file(os.path.join(BASE_DIR, href))
                    if file_topics:
                        for t in file_topics:
                            if not t['title']: t['title'] = link_text
                            t['filename'] = href
                            topics.append(t)

            elif next_node.name == 'font':
                for a in next_node.find_all('a'):
                    href = a.get('href')
                    link_text = clean_text(a.get_text())
                    if href and href not in ['index.html', 'index2.html', '#']:
                        file_topics = parse_linked_file(os.path.join(BASE_DIR, href))
                        if file_topics:
                            for t in file_topics:
                                if not t['title']: t['title'] = link_text
                                t['filename'] = href
                                topics.append(t)
            
            next_node = next_node.next_sibling

        if theme_name:
            themes.append({
                "theme_title": theme_name,
                "topics": topics
            })

    output_data = {
        "volume_title": "経綸・霊主体従・夜昼転換・祖霊祭祀編 (Volume 1)",
        "themes": themes
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved Volume 1 JSON to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
