import json
import os
import re
import backoff
import requests
from typing import Optional, Tuple, List
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tqdm import tqdm

# DeepSeek configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-6c2c1ed44aa94d1a9147547b21e4340c')
DEEPSEEK_MODEL = "deepseek-r1-0528"
MAX_OUTPUT_TOKENS = 8192

# For local model usage (optional)
USE_LOCAL_MODEL = False
LOCAL_MODEL_NAME = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"

class DeepSeekClient:
    def __init__(self, use_local=False):
        self.use_local = use_local
        if use_local:
            print("Loading DeepSeek model locally... (this may take a while)")
            self.tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(
                LOCAL_MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            self.api_url = "https://api.deepseek.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

    def generate(self, prompt, temperature=0.7, max_tokens=MAX_OUTPUT_TOKENS):
        if self.use_local:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True
                )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        else:
            # Use API
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a mathematical research assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']

# Global client instance
deepseek_client = None

def create_client(model: str):
    """Create and return an LLM client."""
    global deepseek_client
    if model.startswith("deepseek"):
        if deepseek_client is None:
            deepseek_client = DeepSeekClient(use_local=USE_LOCAL_MODEL)
        return deepseek_client, model
    else:
        raise ValueError(f"Model {model} not supported")

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException,),
    max_time=600,
)
def get_response_from_llm(
        msg: str,
        client: DeepSeekClient,
        model: str,
        system_message: str,
        print_debug: bool = False,
        msg_history: Optional[List] = None,
        temperature: float = 0.7,
) -> Tuple[str, List]:
    """Get response from DeepSeek."""
    if msg_history is None:
        msg_history = []
    
    # Combine system message and user message
    full_prompt = f"{system_message}\n\nUser: {msg}\n\nAssistant:"
    
    # Generate response
    print("\n🤔 Thinking... (DeepSeek is processing your request)")
    content = client.generate(full_prompt, temperature=temperature)
    
    # Update message history
    new_msg_history = msg_history + [
        {"role": "user", "content": msg},
        {"role": "assistant", "content": content}
    ]
    
    if print_debug:
        print(f"\n📝 User: {msg[:100]}...")
        print(f"🤖 Assistant: {content[:200]}...")
    
    return content, new_msg_history

def extract_json_between_markers(llm_output: str) -> Optional[dict]:
    """Extract JSON from LLM output."""
    # Try to find JSON between ```json and ``` markers
    json_pattern = r"```json\s*(.*?)\s*```"
    matches = re.findall(json_pattern, llm_output, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # Try to find raw JSON
    try:
        # Find JSON object
        start = llm_output.find('{')
        if start >= 0:
            # Find matching closing brace
            count = 1
            i = start + 1
            while i < len(llm_output) and count > 0:
                if llm_output[i] == '{':
                    count += 1
                elif llm_output[i] == '}':
                    count -= 1
                i += 1
            
            if count == 0:
                potential_json = llm_output[start:i]
                return json.loads(potential_json)
    except json.JSONDecodeError:
        pass
    
    return None