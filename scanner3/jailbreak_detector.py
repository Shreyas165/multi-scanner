import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

MODEL_ID = "karthickhps/llm-detect"
BASE_TOKENIZER = "distilbert-base-uncased"
BLOCK_THRESHOLD = 0.95

# --- Load classifier model and tokenizer once ---
print("[JAILBREAK] Loading model and tokenizer...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
model.eval()
tokenizer = AutoTokenizer.from_pretrained(BASE_TOKENIZER)
print("[JAILBREAK] Model and tokenizer loaded.")

# --- Load generator model ---
print("[JAILBREAK] Loading generator...")
generator = pipeline(
    'text-generation',
    model='distilgpt2',
    device=0 if torch.cuda.is_available() else -1
)
print("[JAILBREAK] Generator ready.")


def is_prompt_malicious(prompt: str) -> tuple[str, float]:
    """Returns unsafe/safe and the probability score"""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    prob = torch.softmax(outputs.logits, dim=1)[0][1].item()
    status = "unsafe" if prob > BLOCK_THRESHOLD else "safe"
    return status, round(prob, 4)


def generate_response(prompt: str) -> str:
    """Generates a model response to a prompt"""
    try:
        result = generator(prompt, max_length=100, num_return_sequences=1, temperature=0.7)
        return result[0]['generated_text']
    except Exception as e:
        return f"Generation failed: {str(e)}"
