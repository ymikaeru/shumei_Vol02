import json
import os

BASE_DIR = "/Users/michael/Documents/Ensinamentos/Sites/BR/Shumei_Vol01/Data"
JSON_FILE = os.path.join(BASE_DIR, "shumeic1_part2_data_bilingual.json")

def main():
    if not os.path.exists(JSON_FILE):
        print(f"Error: File not found at {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    themes = data.get("themes", [])
    
    report_lines = []
    report_lines.append("# Relatório de Merge e Tradução")
    report_lines.append(f"**Arquivo Analisado:** `{os.path.basename(JSON_FILE)}`")
    report_lines.append("")
    report_lines.append("| Tema | Título JP | Título PT | Tópicos Traduzidos | Total Tópicos | Progresso |")
    report_lines.append("|---|---|---|---|---|---|")

    total_topics_all = 0
    total_translated_all = 0

    for theme in themes:
        title_jp = theme.get("theme_title", "N/A")
        title_pt = theme.get("theme_title_pt", "N/A")
        topics = theme.get("topics", [])
        
        num_topics = len(topics)
        num_translated = 0
        
        for topic in topics:
            # Check if content_pt exists and is not empty
            if topic.get("content_pt"):
                num_translated += 1
        
        progress = (num_translated / num_topics * 100) if num_topics > 0 else 0
        
        report_lines.append(f"| {title_jp} | {title_jp} | {title_pt} | {num_translated} | {num_topics} | {progress:.1f}% |")
        
        total_topics_all += num_topics
        total_translated_all += num_translated

    report_lines.append("")
    total_progress = (total_translated_all / total_topics_all * 100) if total_topics_all > 0 else 0
    report_lines.append(f"**Total Geral:** {total_translated_all} / {total_topics_all} tópicos traduzidos ({total_progress:.1f}%)")
    
    print("\n".join(report_lines))

if __name__ == "__main__":
    main()
