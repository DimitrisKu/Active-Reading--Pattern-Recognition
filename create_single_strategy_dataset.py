import json
import os
import random

# Set seed for reproducibility
random.seed(42)

input_dir = '/Users/christos/Desktop/Active-Reading--Pattern-Recognition/active_reading_outputs'
output_dir = '/Users/christos/Desktop/Active-Reading--Pattern-Recognition/active_reading_outputs_single_strategy'

# Create output directory
os.makedirs(output_dir, exist_ok=True)

total_original = 0
total_filtered = 0

for filename in os.listdir(input_dir):
    if filename.endswith('.jsonl'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Read all entries
        entries = []
        with open(input_path, 'r') as f:
            for line in f:
                entries.append(json.loads(line))
        
        total_original += len(entries)
        
        # Group by chunk_id
        chunks = {}
        for entry in entries:
            chunk_id = entry['chunk_id']
            if chunk_id not in chunks:
                chunks[chunk_id] = []
            chunks[chunk_id].append(entry)
        
        # Select one strategy per chunk (first one by strategy_id)
        filtered_entries = []
        for chunk_id in sorted(chunks.keys()):
            strategies = chunks[chunk_id]
            # Select the first strategy (lowest strategy_id)
            selected = min(strategies, key=lambda x: x['strategy_id'])
            filtered_entries.append(selected)
        
        total_filtered += len(filtered_entries)
        
        # Write to output file
        with open(output_path, 'w') as f:
            for entry in filtered_entries:
                f.write(json.dumps(entry) + '\n')
        
        print(f'Processed {filename}: {len(entries)} -> {len(filtered_entries)} entries')

print(f'\n{"="*80}')
print(f'Dataset Creation Complete!')
print(f'{"="*80}')
print(f'Original entries: {total_original}')
print(f'Filtered entries: {total_filtered}')
print(f'Reduction: {total_original - total_filtered} entries removed')
print(f'\nOutput directory: {output_dir}')
