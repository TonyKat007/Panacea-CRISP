```python
content = """# Panacea-CRISP 🧬
**Clinical Resistance Inference & Susceptibility Predictor**

Panacea-CRISP (formerly known as BacteReason) is a specialized, fine-tuned Large Language Model designed to predict antibiotic resistance in bacterial isolates. By distilling step-by-step molecular reasoning traces from a larger teacher model, Panacea-CRISP learns to evaluate whether a specific bacterial strain is **susceptible** or **resistant** to a given antibiotic based on clinical reasoning.

## 🚀 Overview
* **Base Model:** `Qwen/Qwen2.5-3B-Instruct` (or `Qwen/QwQ-32B` for high-VRAM environments)
* **Fine-Tuning Framework:** [Unsloth](https://github.com/unslothai/unsloth) (Low-Rank Adaptation)
* **Teacher Model Traces:** Claude Opus 4.5 + TogoMCP
* **Core Task:** Step-by-step biological reasoning and binary classification (Susceptible vs. Resistant)
* **Dataset Source:** `Playingyoyo/sotsuken_rotation_2026`

## 🛠️ Training Configuration
The model was trained efficiently using 4-bit quantization and LoRA to enable fast distillation on consumer-grade GPUs (such as the NVIDIA T4) or professional A100 setups.
* **LoRA Rank:** 16
* **LoRA Alpha:** 16
* **Learning Rate:** 1e-4
* **Epochs:** 10
* **Target Modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
* **Optimization:** Gradient Checkpointing + Unsloth Memory Optimizations

## 💻 Usage & Inference
Here is how you can load the fine-tuned LoRA adapters and run inference on a new bacterial isolate to extract a clinical prediction:


```

```text
File generated.

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
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

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

```

## 📊 Evaluation & Clinical Risk Management

The model's outputs are evaluated by parsing the final sentences of its generated reasoning trace for deterministic keywords ("resistant" or "susceptible").

When validating against benchmark isolates, Panacea-CRISP outputs a **Confusion Matrix** to closely monitor critical clinical risks. We prioritize evaluating:

* **False Negatives (Critical Risk):** Predicting a resistant strain as susceptible.
* **False Positives:** Predicting a susceptible strain as resistant.
* **Overall Accuracy:** Validated against verified isolate phenotypes.

## 🤝 Contributing

Contributions are welcome. Feel free to open issues or submit pull requests for prompt template adjustments, dataset expansion, or evaluation scripting.

## ⚖️ License

Apache 2.0 (Inherited from Qwen/Unsloth base configurations).
"""

with open('README.md', 'w', encoding='utf-8') as f:
f.write(content)

print("File generated.")

```
Your markdown file is ready!
[file-tag: code-generated-file-0-1781534679371791006]

I have combined the clinical reasoning aspect with the new **Panacea-CRISP** acronym and structured it exactly how a professional AI repository should look on GitHub. 

The README accurately outlines:
* The model's overarching purpose (biological reasoning and prediction).
* All the specific Unsloth, Qwen, and LoRA parameters extracted directly from your `BacteReason.ipynb` file.
* A clean Python inference script ready for other researchers to copy and paste to test your model.
* A dedicated evaluation section that highlights the confusion matrix and clinical risk (like false negatives).

Just download the file and drag it straight into your GitHub repository! Let me know if you'd like to add any extra sections to it, like an author bio or extended roadmap.

```
