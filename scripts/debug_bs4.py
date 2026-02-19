from bs4 import BeautifulSoup
import os

html = """
<BLOCKQUOTE>
<BLOCKQUOTE>
<BLOCKQUOTE><BR>
<B><FONT size="+2">明主様御講話　「大光明世界の建設」</FONT></B>　（昭和10年2月4日発行）<BR>
<BR>
"""

soup = BeautifulSoup(html, 'html.parser')
title_font = soup.find('font', size='+2')

print(f"Title Font: {title_font}")
print(f"Parent: {title_font.parent.name}")
print(f"Parent Text: {title_font.parent.get_text()}")
print(f"Parent Next Sibling: {repr(title_font.parent.next_sibling)}")
print(f"Is string? {isinstance(title_font.parent.next_sibling, str)}")

candidates = []
if title_font.parent:
    candidates.append(title_font.parent.get_text())
    if title_font.parent.next_sibling:
        # Convert to string to be safe
        candidates.append(str(title_font.parent.next_sibling))

print(f"Candidates: {candidates}")

import re
date = ""
for cand in candidates:
    date_match = re.search(r'（(.*?)）', cand)
    if date_match:
        date = date_match.group(1)
        break
print(f"Date: {date}")
