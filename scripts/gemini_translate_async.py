import os
import json
import glob
import time
import argparse
import asyncio
import google.generativeai as genai

# Max concurrent requests to send to the Gemini API
CONCURRENCY_LIMIT = 50 

def is_already_translated(input_file, output_dir):
    """Verifica se o arquivo já foi traduzido verificando se a chave content_ptbr ou title_ptbr existe."""
    basename = os.path.basename(input_file)
    expected_output = os.path.join(output_dir, basename)
    if not os.path.exists(expected_output):
        return False
        
    try:
        with open(expected_output, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return "content_ptbr" in data[0]
            elif isinstance(data, dict):
                topics = data.get("topics", [])
                if len(topics) > 0:
                    return "content_ptbr" in topics[0]
    except Exception:
        return False
        
    return False

async def translate_file_async(input_path, output_path, model, semaphore):
    """
    Translates a JSON file using the Gemini Pro API asynchronously.
    """
    async with semaphore:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
                if isinstance(input_data, list):
                    input_str = json.dumps({"topics": input_data}, ensure_ascii=False)
                else:
                    input_str = json.dumps(input_data, ensure_ascii=False)
        except Exception as e:
            print(f"ERRO ao ler {input_path}: {e}")
            return False

        print(f"🚀 Iniciando Tradução: {os.path.basename(input_path)}...", flush=True)

        try:
            # We use asyncio.to_thread to run the synchronous SDK call in a separate thread
            # so it doesn't block the asyncio event loop
            response = await asyncio.to_thread(
                model.generate_content, 
                input_str, 
                request_options={"timeout": 600}
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                try:
                    parsed = json.loads(response.text)
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
                    print(f"✅ Sucesso -> {os.path.basename(output_path)}", flush=True)
                except json.JSONDecodeError:
                    f.write(response.text)
                    print(f"⚠️ Salvo (Mas não é JSON estrito) -> {os.path.basename(output_path)}", flush=True)
                    
            return True
        
        except Exception as e:
            print(f"❌ ERRO na API para {os.path.basename(input_path)}: {e}", flush=True)
            return False

async def translate_directory_async(input_dir, output_dir, prompt_path, pattern="theme_05_*.json"):
    """Traduz todos os arquivos de um diretório matching o padrão de forma assíncrona."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERRO: A variável de ambiente GEMINI_API_KEY conf não existe!")
        return

    genai.configure(api_key=api_key)

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_instruction = f.read()
    except FileNotFoundError:
        print(f"ERRO: Arquivo de prompt não encontrado: {prompt_path}")
        return

    model = genai.GenerativeModel(
        model_name="gemini-3.1-pro-preview",
        system_instruction=system_instruction,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json",
        ),
        safety_settings={
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        }
    )

    search_pattern = os.path.join(input_dir, pattern)
    files_to_process = sorted(glob.glob(search_pattern))
    
    if not files_to_process:
        print(f"Nenhum arquivo encontrado em {search_pattern}")
        return

    print(f"Encontrados {len(files_to_process)} arquivos para traduzir.")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Coletar arquivos pendentes
    pending_files = []
    skip_count = 0

    for input_file in files_to_process:
        if is_already_translated(input_file, output_dir):
            skip_count += 1
        else:
            pending_files.append(input_file)
            
    print(f"[{skip_count}/{len(files_to_process)}] Arquivos pulados (já traduzidos).")
    print(f"Restam {len(pending_files)} arquivos para traduzir.")

    if not pending_files:
        print("Tudo já está traduzido!")
        return

    start_time = time.time()
    
    # Criar um semáforo para limitar a concorrência
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    # Criar e rodar as tarefas assíncronas
    tasks = []
    for input_file in pending_files:
        output_file = os.path.join(output_dir, os.path.basename(input_file))
        tasks.append(translate_file_async(input_file, output_file, model, semaphore))

    print(f"Iniciando execuções simultâneas em lotes de {CONCURRENCY_LIMIT}...")
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r)
    
    end_time = time.time()
    elapsed = end_time - start_time

    print("-" * 30)
    print(f"Processo Concluído!")
    print(f"Tempo total para novos: {elapsed:.2f} segundos")
    print(f"Traduzidos: {success_count}")
    print(f"Mantecidos/Pulados: {skip_count}")

def main():
    parser = argparse.ArgumentParser(description="Script para traduzir múltiplos arquivos em PARALELO com a API do Gemini Pro")
    parser.add_argument("--input_dir", "-i", default="Data/parts_for_translation", help="Diretório dos arquivos originais")
    parser.add_argument("--output_dir", "-o", default="Data/translated_parts", help="Diretório para salvar traduções")
    parser.add_argument("--prompt", "-p", default="PROMPT_TRANSLACAO_VOL2.md", help="Arquivo de prompt")
    parser.add_argument("--pattern", "-m", default="theme_05_*.json", help="Padrão de busca (ex: theme_05_*.json)")
    
    args = parser.parse_args()
    
    asyncio.run(translate_directory_async(args.input_dir, args.output_dir, args.prompt, args.pattern))

if __name__ == "__main__":
    main()
