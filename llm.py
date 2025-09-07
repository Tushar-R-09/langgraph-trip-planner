from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# Chat-style formatting for TinyLlama
def format_chat_prompt(user_prompt: str) -> str:
    return f"<|system|>\nYou are a helpful travel planning assistant.\n<|user|>\n{user_prompt}\n<|assistant|>"

# Create text-generation pipeline
llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=800,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

def llm(prompt: str) -> str:
    """Generate text using TinyLlama with proper chat formatting."""
    chat_prompt = format_chat_prompt(prompt)
    outputs = llm_pipeline(chat_prompt, return_full_text=False)
    return outputs[0]["generated_text"].strip()
