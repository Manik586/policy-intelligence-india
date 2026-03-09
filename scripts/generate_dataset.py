import os
import json
import time
import re
from huggingface_hub import InferenceClient
from google.colab import userdata, files

# 1. Setup Client
client = InferenceClient(api_key=userdata.get('HF_TOKEN'))

# 2. Files
text_file = "combined_circular_economy_data.txt"
output_file = "circular_economy_dataset.jsonl"

def generate_robust_dataset(text_file, output_file):
    with open(text_file, 'r') as f:
        content = f.read()

    chunks = [content[i:i+8000] for i in range(0, len(content), 8000)]

    # RESUME LOGIC: Detects existing lines and starts exactly where you left off
    start_chunk = 0
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            lines = f.readlines()
            start_chunk = len(lines) // 5
        print(f" Resuming from chunk {start_chunk + 1}...")

    for i in range(start_chunk, len(chunks)):
        chunk = chunks[i]
        prompt = f"Return ONLY a JSON list of 5 Instruction-Output pairs from this text: {chunk}"

        success = False
        while not success: # FIX: Infinite retry ensures no chunk is ever skipped
            try:
                response = client.chat_completion(
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )

                raw_text = response.choices[0].message.content

                # THE FIX: Use Regex to find the JSON list even if there is 'Extra data'
                match = re.search(r'\[.*\]', raw_text, re.DOTALL)
                if match:
                    clean_json = match.group(0)
                    pairs = json.loads(clean_json) #

                    with open(output_file, 'a') as f:
                        for entry in pairs:
                            f.write(json.dumps(entry) + '\n')

                    print(f" Chunk {i+1}/{len(chunks)} saved successfully.")
                    success = True # Move to the next chunk
                    time.sleep(12) # Safety delay for free tier
                else:
                    raise ValueError("AI failed to output a valid JSON list format.")

            except Exception as e:
                # Handle 503 (Busy) and 429 (Rate Limit) by waiting and retrying
                print(f" Issue at {i+1}: {e}. Retrying same chunk in 60s...")
                time.sleep(60)

generate_robust_dataset(text_file, output_file)