
import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
MAIN_JSON = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")
TRANSLATIONS_JSON = os.path.join(BASE_DIR, "remaining_untranslated_translated.json")

def main():
    if not os.path.exists(MAIN_JSON) or not os.path.exists(TRANSLATIONS_JSON):
        print("Error: Input files not found.")
        return

    print(f"Loading main JSON: {MAIN_JSON}")
    with open(MAIN_JSON, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    print(f"Loading translations: {TRANSLATIONS_JSON}")
    with open(TRANSLATIONS_JSON, 'r', encoding='utf-8') as f:
        trans_data = json.load(f)

    # Index main data for faster lookup? 
    # Since specific match requires iterating themes, let's just iterate.
    # We can create a map of (filename, title) -> topic_object
    
    topic_map = {}
    total_main_topics = 0
    
    if "themes" in main_data:
        for theme in main_data["themes"]:
            if "topics" in theme:
                for topic in theme["topics"]:
                    # Create a unique key. Filename + Title is usually sufficient.
                    # Some files have multiple topics with same title? (e.g. "Order")
                    # Let's use filename + title + date just to be sure.
                    key = (topic.get("filename", ""), topic.get("title", ""), topic.get("date", ""))
                    topic_map[key] = topic
                    total_main_topics += 1

    print(f"Indexed {total_main_topics} topics from main JSON.")

    print(f"Loading original reference: {os.path.join(BASE_DIR, 'remaining_untranslated.json')}")
    with open(os.path.join(BASE_DIR, 'remaining_untranslated.json'), 'r', encoding='utf-8') as f:
        reference_data = json.load(f)
    
    reference_topics = reference_data.get("topics", [])
    
    if isinstance(trans_data, list):
        trans_topics = trans_data
    else:
        trans_topics = trans_data.get("topics", [])

    if len(reference_topics) != len(trans_topics):
        print(f"Warning: Reference topics count ({len(reference_topics)}) does not match translated topics count ({len(trans_topics)}). Sync might be lost.")
    
    updates_count = 0
    skipped_count = 0

    # Build a lookup list of topics from main data for efficient search
    # We will search by (filename, content)
    main_topics_list = []
    if "themes" in main_data:
        for theme in main_data["themes"]:
            for topic in theme.get("topics", []):
                main_topics_list.append(topic)

    for i, ref_item in enumerate(reference_topics):
        if i >= len(trans_topics):
            break
            
        trans_item = trans_topics[i]
        ref_filename = ref_item.get("filename")
        ref_content_jp = ref_item.get("content")
        
        # Search for the topic in main JSON that matches filename and Japanese content
        target_topic = None
        for topic in main_topics_list:
            if topic.get("filename") == ref_filename and topic.get("content") == ref_content_jp:
                target_topic = topic
                break
        
        if target_topic:
            # Update fields if present in translation and non-empty
            updated = False
            
            new_title_pt = trans_item.get("title_pt", "").strip() or trans_item.get("title_ptbr", "").strip()
            new_content_pt = trans_item.get("content_pt", "").strip() or trans_item.get("content_ptbr", "").strip()
            new_pub_title = trans_item.get("publication_title_pt", "").strip() or trans_item.get("publication_title_ptbr", "").strip()
            
            if new_title_pt:
                if target_topic.get("title_pt") != new_title_pt:
                    target_topic["title_pt"] = new_title_pt
                    updated = True

            if new_content_pt:
                if target_topic.get("content_pt") != new_content_pt:
                    target_topic["content_pt"] = new_content_pt
                    updated = True
            
            if new_pub_title:
                if target_topic.get("publication_title_pt") != new_pub_title:
                    target_topic["publication_title_pt"] = new_pub_title
                    updated = True
            
            if updated:
                updates_count += 1
                # print(f"Updated: {ref_item.get('title')}")
            else:
                skipped_count += 1
        else:
            print(f"Warning: Topic not found in main JSON: {ref_item.get('title')} ({ref_item.get('filename')})")

    print(f"Merge complete. Updated {updates_count} topics. Skipped/Unchanged {skipped_count} topics.")

    # Save back
    with open(MAIN_JSON, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    print(f"Saved updated JSON to {MAIN_JSON}")

if __name__ == "__main__":
    main()
