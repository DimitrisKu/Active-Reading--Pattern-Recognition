import json
import os
import random
from collections import defaultdict

input_dir = "/Users/christos/Desktop/Active-Reading--Pattern-Recognition/generated_simplewiki/active_reading_outputs"
output_file = "/Users/christos/Desktop/Active-Reading--Pattern-Recognition/Finetune_Datasets/simplewiki/active_reading_single_dataset.jsonl"

# Group entries by doc_name and chunk_id
entries_by_chunk = defaultdict(list)

# Process all JSONL files
for filename in os.listdir(input_dir):
    if filename.endswith('.jsonl'):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r') as f:
            for line in f:
                entry = json.loads(line)
                key = (entry['doc_name'], entry['chunk_id'])
                entries_by_chunk[key].append(entry)

print(f"Found {len(entries_by_chunk)} unique chunks")

# Select first strategy (min by strategy_id) for each chunk
filtered_entries = []
for (doc_name, chunk_id), entries in entries_by_chunk.items():
    # Sort by strategy_id and take the first one
    first_strategy = min(entries, key=lambda x: x['strategy_id'])
    # Keep only doc_name and active_reading
    filtered_entries.append({
        'doc_name': first_strategy['doc_name'],
        'active_reading': first_strategy['active_reading']
    })

print(f"Selected {len(filtered_entries)} entries (one per chunk)")

# Shuffle for training
random.seed(42)
random.shuffle(filtered_entries)

# Write output
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    for entry in filtered_entries:
        f.write(json.dumps(entry) + '\n')

print(f"Written to {output_file}")
print(f"First 5 doc_names (after shuffle): {[e['doc_name'] for e in filtered_entries[:5]]}")
