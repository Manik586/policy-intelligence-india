from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import os

# 1. Load the optimized Gemma 3 model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/gemma-3-4b-it",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Updated LoRA with higher capacity (Verified for Policy Intelligence)
model = FastLanguageModel.get_peft_model(
    model,
    r = 32, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"], 
    lora_alpha = 32, 
    lora_dropout = 0,
    bias = "none",
)

# 3. Load your formatted dataset from the PROCESSED folder
dataset = load_dataset("json", data_files="data/processed/unsloth_dataset.json", split="train")

# 4. Updated Training Config for deeper learning
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 150, 
        learning_rate = 1e-4, 
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        weight_decay = 0.01, 
        output_dir = "evals/training_outputs", # Save logs to the evals folder
    ),
)

# 5. Run Training
print(" Starting Fine-Tuning...")
trainer.train()

# 6. Save the final "Intelligence" adapters
model.save_pretrained("policy_intelligence_model_v1")
tokenizer.save_pretrained("policy_intelligence_model_v1")
print(" Saved successfully to: policy_intelligence_model_v1")