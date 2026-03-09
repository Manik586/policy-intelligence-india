from unsloth import FastLanguageModel
import torch

# 1. Load the model for inference
# We point to your local 'policy_intelligence_v1' folder
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "policy_intelligence_v1", # The folder where you saved the weights
    max_seq_length = 2048,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)

# 2. Setup the test question
instruction = "What are the specific NITI Aayog recommendations for the 'circularity' of End-of-Life Vehicles (ELVs) in India?"
prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Response:
{}"""

# 3. Process inputs
inputs = tokenizer([prompt.format(instruction, "")], return_tensors = "pt").to("cuda")

# 4. Generate the response using your "Looping Fix"
print(" Generating Response...")
outputs = model.generate(
    **inputs,
    max_new_tokens = 512,
    temperature = 0.7,      # Higher temperature = more creativity
    top_p = 0.9,            # Only considers the top 90% most likely words
    repetition_penalty = 1.2 # The breakthrough fix to stop looping
)

# 5. Output the results
result = tokenizer.decode(outputs[0], skip_special_tokens = True)
print("-" * 30)
print(result)