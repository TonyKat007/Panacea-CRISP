# Panacea-CRISP 🧬
**Clinical Resistance Inference & Susceptibility Predictor**

Panacea-CRISP (formerly known as BacteReason) is a specialized, fine-tuned Large Language Model designed to predict antibiotic resistance in bacterial isolates. By distilling step-by-step molecular reasoning traces from a larger teacher model, Panacea-CRISP learns to evaluate whether a specific bacterial strain is **susceptible** or **resistant** to a given antibiotic based on complex clinical reasoning.

---

## 🚀 Overview
* **Base Model:** `Qwen/Qwen2.5-3B-Instruct` (or `Qwen/QwQ-32B` for high-VRAM environments)
* **Fine-Tuning Framework:** [Unsloth](https://github.com/unslothai/unsloth) (Low-Rank Adaptation)
* **Teacher Model Traces:** Claude Opus 4.5 + TogoMCP
* **Core Task:** Step-by-step biological reasoning and binary classification (Susceptible vs. Resistant)
* **Dataset Source:** `Playingyoyo/sotsuken_rotation_2026`

---

## 🛠️ Training Configuration
The model was trained efficiently using 4-bit quantization and LoRA to enable fast distillation on consumer-grade GPUs (such as the NVIDIA T4) or professional A100 setups.
* **LoRA Rank:** 16
* **LoRA Alpha:** 16
* **Learning Rate:** 1e-4
* **Epochs:** 10
* **Target Modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
* **Optimization:** Gradient Checkpointing + Unsloth Memory Optimizations

---

## 💻 Usage & Inference
Here is how you can load the fine-tuned LoRA adapters and run inference on a new bacterial isolate to extract a clinical prediction:

```python
from unsloth import FastLanguageModel
import torch

# Configuration
max_seq_length = 4096
# Replace this with your actual local adapter path or Hugging Face repo ID
model_path = "YOUR_GITHUB_USERNAME/Panacea-CRISP" 

print("Loading Panacea-CRISP...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_path,
    max_seq_length=max_seq_length,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

# Prepare Input
question = "Given the biosample SAMN14755011, is the species Escherichia coli susceptible or resistant to ceftriaxone?"
messages = [{"role": "user", "content": question}]
input_text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True, # Forces the model to generate the assistant's response
)
inputs = tokenizer(input_text, return_tensors=\"pt\").to(model.device)

# Generate Reasoning & Prediction
print("Generating clinical reasoning trace...")
with torch.no_grad():
    output_ids = model.generate(
        **inputs,
        max_new_tokens=2048,
        do_sample=False, # Greedy decoding for deterministic, reproducible reasoning
    )

new_tokens = output_ids[0][inputs["input_ids"].shape[-1]:]
generated_trace = tokenizer.decode(new_tokens, skip_special_tokens=True)

print("\\n=== Final Reasoning & Verdict ===")
print(generated_trace)
