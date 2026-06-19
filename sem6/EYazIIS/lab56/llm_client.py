# llm_client.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class LocalLLM:
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        print("Loading Qwen model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        
        print("Qwen ready!")
    
    def generate_answer(self, question: str, context: str) -> str:
        """Force English answer from Qwen"""
        
        prompt = f"""<|im_start|>system
You are an English-only assistant. NEVER use Russian, Ukrainian, or any other language. 
ONLY respond in English. If you see Russian text, ignore it and respond in English. Use context from documents.
<|im_end|>
<|im_start|>user
Here is the context from documents:

{context}

Question: {question}

IMPORTANT: Answer ONLY in English. Do not write a single word in Russian.
<|im_end|>
<|im_start|> assistantt
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1800)
        
        if self.device == "cuda":
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.5, 
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Убираем промпт из ответа
        response = response.split("assistantt")[-1].strip()
        
        
        return response if response else "No information found in the documents."