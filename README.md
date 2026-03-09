# Policy Intelligence India 
### Fine-tuning Gemma-3-4B-IT for Circular Economy Regulatory Analysis

Policy Intelligence India is a specialized AI system designed to analyze and interpret complex Indian regulatory frameworks. This project specifically targets the **2025-2026 Circular Economy Roadmaps** from **NITI Aayog** and the **Ministry of Environment, Forest and Climate Change (MoEF&CC)**.

By leveraging **Unsloth** and **LoRA**, this model achieves high factual precision in policy analysis while overcoming common small-model issues like repetitive generation loops.

---

## Technical Highlights
* **Base Model:** Gemma-3-4B-IT.
* **Optimization:** 4-bit quantization via Unsloth for efficient T4 GPU utilization.
* **Fine-Tuning:** PEFT/LoRA (Rank: 32, Alpha: 32) targeting all linear projections.
* **Performance:** Achieved a **0.65 training loss** over 150 steps.
* **The "Looping Fix":** Implemented a specialized inference configuration (Repetition Penalty: 1.2, Temperature: 0.7) to ensure structured, non-repetitive policy reports.

---

##  Repository Structure
```text
├── core/             # Modular prompts and recovery utilities
├── data/             
│   ├── processed/    # Cleaned training data (unsloth_dataset.json)
│   └── samples/      # Preview examples for transparency
├── evals/            # Benchmark tasks and model performance reports
├── scripts/          # Automated training and dataset generation scripts
└── requirements.txt  # Environment dependencies