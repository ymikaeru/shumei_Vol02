
import json

def check_missing_translations(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    print(f"Data type: {type(data)}")
    
    target_list = []
    

    if "themes" in data and isinstance(data["themes"], list):
        print(f"Found {len(data['themes'])} themes.")
        
        # Check keys of first theme to find the articles list
        if len(data["themes"]) > 0:
            print(f"First theme keys: {list(data['themes'][0].keys())}")
            
        total_articles = 0
        missing_count = 0
        missing_items = []

        for theme_idx, theme in enumerate(data["themes"]):
            # Find the list inside the theme
            articles_list = []
            for key, value in theme.items():
                if isinstance(value, list):
                    articles_list = value
                    break
            
            if not articles_list:
                print(f"Warning: No list found in theme {theme_idx}")
                continue

            for item in articles_list:
                if not isinstance(item, dict):
                    continue
                
                total_articles += 1
                
                # Check translation
                has_pt = "content_pt" in item and item["content_pt"] and str(item["content_pt"]).strip() != ""
                # Also check title just in case
                has_title_pt = "title_pt" in item and item["title_pt"] and str(item["title_pt"]).strip() != ""

                if not (has_pt or has_title_pt): # If NEITHER is present, count as missing
                    # Actually, we really want content. But some items might be just titles?
                    # Let's stick to content for now as strict check.
                    if not has_pt:
                         missing_count += 1

                         missing_items.append({
                            "theme_index": theme_idx,
                            "title": item.get("title", "No Title"),
                            "filename": item.get("filename", "No Filename"),
                             "date": item.get("date", "No Date"),
                             "content": item.get("content", "")
                         })



        print("-" * 30)
        print(f"Total articles analyzed: {total_articles}")
        print(f"Missing translations: {missing_count}")
        print("-" * 30)
        
        # Save missing items to a file for translation
        if missing_count > 0:
            output_file = "missing_translations.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(missing_items, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(missing_items)} missing items to {output_file}")

        if missing_count > 0:
            print("First 50 missing items:")

            for i, item in enumerate(missing_items):
                print(f"{i+1}. [Theme {item['theme_index']}] {item['title']} ({item['filename']})")
                if i >= 49:
                    print(f"... and {len(missing_items) - 50} more.")
                    break
    
    else:
        print("Structure is not as expected (no 'themes' key).")


if __name__ == "__main__":
    file_path = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data/shumeic1_part2_data_bilingual.json"
    check_missing_translations(file_path)
