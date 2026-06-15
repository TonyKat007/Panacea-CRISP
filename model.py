import os
import spaces
import torch
from threading import Thread
from transformers import AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
from peft import AutoPeftModelForCausalLM

MODEL_ID = "Playingyoyo/BacteReason"
HF_TOKEN = os.environ.get("HF_TOKEN")
MAX_NEW_TOKENS = 4096  # paper traces are typically 1,500-5,000 tokens

model = None
tokenizer = None


def load_model():
    global model, tokenizer
    print(f"Loading Model: {MODEL_ID}...")

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )

    try:
        model = AutoPeftModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=quantization_config,
            device_map="auto",
            token=HF_TOKEN,
        )
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id
        model.eval()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")


@spaces.GPU(duration=600)
def run_inference_stream(question):
    """Generator that yields the accumulated reasoning trace as tokens are produced."""
    global model, tokenizer

    if model is None:
        load_model()
    if model is None:
        yield "❌ Model failed to load. Check Space logs."
        return

    messages = [{"role": "user", "content": question}]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(
        [input_text], return_tensors="pt", truncation=True, max_length=8192,
    ).to("cuda")

    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=60,
    )

    generation_kwargs = dict(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,
        streamer=streamer,
        pad_token_id=tokenizer.eos_token_id,
        use_cache=True,
    )

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    accumulated = ""
    for new_text in streamer:
        accumulated += new_text
        yield accumulated