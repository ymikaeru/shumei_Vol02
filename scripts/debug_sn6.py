
import os
import re
from bs4 import BeautifulSoup

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def debug_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    font_tags = soup.find_all('font', size='+2')

    print(f"Found {len(font_tags)} font tags with size=+2")

    valid_headers = []
    for i, ft in enumerate(font_tags):
        text = ft.get_text(strip=True)
        print(f"[{i}] Text: {text[:30]}... | Parent: {ft.parent.name}")
        
        # Check nesting
        parents = list(ft.parents)
        is_nested = any(p in [vh['node'] for vh in valid_headers] for p in parents)
        print(f"    Nested in previous Valid Header? {is_nested}")

        valid_headers.append({
            'node': ft,
            'title': text
        })

    # Simulate splitting logic
    print("\n--- Simulation ---")
    
    # Filter out nested ones
    final_headers = []
    for h in valid_headers:
        is_nested = False
        for existing in final_headers:
            if existing['node'] in h['node'].parents:
                is_nested = True
                break
        if not is_nested:
            final_headers.append(h)
    
    print(f"Fixed Header Count: {len(final_headers)}")

    # Marker insertion strategy equivalent
    # We can't easily do the actual soup modification in this debug script without replicating everything.
    # But we can try to replicate the Text Cleaning logic check.
    
    # Let's look at the first header and what comes after it.
    if len(final_headers) > 1:
        h0 = final_headers[0]
        h1 = final_headers[1]
        
        # In current script logic, content is everything from h0 to h1.
        # But we need the RAW HTML between them.
        
        # Let's try to get text between them in a hacky way for debug
        # Just use output from the user provided snippet as a test case?
        
        # User snippet content:
        raw_content_sample = """<font color="#0000ff" face="メイリオ" size="+2">観世音菩薩について　2　（観音の千変万化的性格について）</font><br/>
</font><br/>
</p>
<blockquote>
<blockquote>
<blockquote><br/>"""
        
        print(f"\nScanning Topic 0: {h0['title']}")
        
        content_soup = BeautifulSoup(raw_content_sample, 'html.parser')
        body_text = clean_text(content_soup.get_text())
        title_text = clean_text(h0['title'])
        
        print(f"Body Text: '{body_text}'")
        print(f"Title Text: '{title_text}'")
        
        remainder = body_text.replace(title_text, '', 1).strip()
        print(f"Remainder after title strip: '{remainder}'")
        print(f"Remainder Len: {len(remainder)}")
        
        if len(remainder) < 5:
            print("FILTER DECISION: SKIP")
        else:
            print("FILTER DECISION: KEEP")

    # Also check actual file content if possible
    # But constructing the split is hard without the markers.
    # We will assume the snippet provided by user IS roughly what the split produced.

if __name__ == "__main__":
    debug_parse("shumeic1/kanzeon2.html")
