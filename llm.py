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
    return f"""<|system|>
            You are a helpful travel planning assistant.

            Return the itinerary in **Markdown format only** like this:

            ### Day 1
            - Morning: ...
            - Afternoon: ...
            - Evening: ...
            💰 Total cost: $...

            ### Day 2
            - Morning: ...
            - Afternoon: ...
            - Evening: ...
            💰 Total cost: $...

            {user_prompt}
            <|assistant|>"""


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
    """Generate JSON itinerary using TinyLlama with strict chat formatting."""
    chat_prompt = format_chat_prompt(prompt)
    outputs = llm_pipeline(chat_prompt, return_full_text=False)
    return outputs[0]["generated_text"].strip()
