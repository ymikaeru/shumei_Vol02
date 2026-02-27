import os
import json
from bs4 import BeautifulSoup, NavigableString

DATA_DIR = './Data'
TRANSLATED_INDEXES_DIR = os.path.join(DATA_DIR, 'translated_indexes')

VOLUMES = [
    {'id': 'shumeic1', 'file': 'shumeic1_data_bilingual.json', 'idx': 'index2.html'},
    {'id': 'shumeic3', 'file': 'shumeic3_data_bilingual.json', 'idx': 'index.html'}
]

def extract_themes_from_html(filepath, vol_id):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
        
    try:
        with open(filepath, 'r', encoding='shift_jis') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
    soup = BeautifulSoup(html, 'html.parser')
    themes = []
    
    for font in soup.find_all('font'):
        text = ""
        if vol_id == 'shumeic1':
            color = font.get('color')
            if color == '#0000ff':
                text = font.get_text().replace('\n', ' ').strip()
        elif vol_id == 'shumeic3':
            if len(font.contents) > 0 and isinstance(font.contents[0], NavigableString):
                text = font.contents[0].replace('\n', ' ').strip()
                
        if text:
            text = text.replace('　', ' ').replace('\r', '').strip()
            # Ignore some specific known boilerplate
            skip_terms = ["通信カレッジ", "Curso por", "Seção da Fé", "Plano Divino・Espírito", "Outros"]
            if any(term in text for term in skip_terms):
                continue
            themes.append(text)
            
    return themes

for vol in VOLUMES:
    vol_id = vol['id']
    json_path = os.path.join(DATA_DIR, vol['file'])
    
    ja_html_path = os.path.join('OrigianlHTML', vol_id, vol['idx'])
    pt_html_path = os.path.join(TRANSLATED_INDEXES_DIR, vol_id, vol['idx'])
    
    ja_themes = extract_themes_from_html(ja_html_path, vol_id)
    pt_themes = extract_themes_from_html(pt_html_path, vol_id)
    
    print(f"Volume {vol_id}: Found {len(ja_themes)} JA themes, {len(pt_themes)} PT themes")
    
    if len(ja_themes) != len(pt_themes):
        print(f"WARNING: Theme count mismatch for {vol_id}")
        print("JA Themes:", ja_themes)
        print("PT Themes:", pt_themes)
    else:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated = 0
        for i, theme in enumerate(data.get('themes', [])):
            if i < len(pt_themes):
                theme['theme_title_pt'] = pt_themes[i]
                theme['theme_title'] = ja_themes[i]
                updated += 1
                
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully updated {updated} themes in {vol['file']}")
