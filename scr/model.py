import transformers
import torch

# model_id = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"
# model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
model_id = "meta-llama/Llama-3.2-3B-Instruct"
# model_id = "5CD-AI/Vintern-1B-v2"
# model_id = "Groq/Llama-3-Groq-8B-Tool-Use"
pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    device= 0,
    model_kwargs={
        "torch_dtype": torch.float16,
        # "quantization_config": {"load_in_4bit": True},
        "low_cpu_mem_usage": True,
    },
    trust_remote_code=True
)
def llama(prompt, temp = 0.1, topk = 5, topp = 0.1):
    prompt = prompt.replace("object", "dict")

    outputs = pipeline(
        prompt,
        max_new_tokens=2048,
        temperature=temp,
        top_k=topk
    )
    response_message = outputs[0]["generated_text"][len(prompt):]
    return response_message