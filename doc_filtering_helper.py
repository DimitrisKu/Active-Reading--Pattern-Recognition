import os
import json
import re

def normalize(name):
    ### Only letters and numbers ###
    if not name:
        return ""
    # re.sub(r'\W+', '', ...) αφαιρεί οτιδήποτε δεν είναι αλφαριθμητικό
    return re.sub(r'[^a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff]', '', str(name)).lower()

def get_names_from_concatenated_file(file_path):
    name_map = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        decoder = json.JSONDecoder()
        while content:
            content = content.lstrip()
            if not content: break
            try:
                obj, index = decoder.raw_decode(content)
                if isinstance(obj, dict) and 'doc_name' in obj:
                    original = obj['doc_name'].strip()
                    name_map[normalize(original)] = original
                content = content[index:].lstrip()
            except json.JSONDecodeError:
                next_start = content.find('{', 1)
                if next_start == -1: break
                content = content[next_start:]
    except Exception:
        pass
    return name_map

def filter_dataset():
    home = os.path.expanduser("~")
    downloads_path = os.path.join(home, "Downloads")
    
    folders = [
        os.path.join(downloads_path, 'generated_simplewiki/active_reading_outputs'),
        os.path.join(downloads_path, 'generated_simplewiki/paraphrase_outputs'),
        os.path.join(downloads_path, 'generated_simplewiki/synthetic_qa_outputs')
    ]
    master_path = os.path.join(downloads_path, 'Datasets/simple_wiki_corpus.json')
    output_path = os.path.join(downloads_path, 'filtered_doc_names_sw.json')

    if not os.path.exists(master_path):
        print(f"Master file not found at: {master_path}")
        return
        
    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)
    
    master_map = {normalize(item['doc_name']): item['doc_name'] for item in master_data if 'doc_name' in item}
    current_intersection = set(master_map.keys())
    
    print(f"--- Initialization ---")
    print(f"Total unique docs in Master: {len(current_intersection)}")

    for i, folder in enumerate(folders, 1):
        folder_name = os.path.basename(folder)
        names_in_folder_normalized = set()
        
        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.lower().endswith(('.json', '.jsonl'))]
            for filename in files:
                file_names_map = get_names_from_concatenated_file(os.path.join(folder, filename))
                names_in_folder_normalized.update(file_names_map.keys())
            
            print(f"\n--- Folder {i}: {folder_name} ---")
            print(f"Found {len(names_in_folder_normalized)} unique alfanumeric names.")
            
            current_intersection = current_intersection.intersection(names_in_folder_normalized)
            print(f"Intersection count: {len(current_intersection)}")
        else:
            print(f"\n--- Folder {i}: {folder_name} (NOT FOUND) ---")
            current_intersection = set()

    final_list = sorted([master_map[name] for name in current_intersection])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"\n--- Final Results ---")
    print(f"Total common doc names saved: {len(final_list)}")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    filter_dataset()
