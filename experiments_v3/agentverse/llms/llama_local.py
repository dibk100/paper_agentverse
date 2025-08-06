# agentverse/llms/llama_local.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LlamaLocalLLM:
    def __init__(self, model_name="meta-llama/Llama-3-8B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model.eval()

    def chat(self, messages, max_tokens=512, temperature=0.7):
        prompt = self.build_prompt(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.postprocess_response(prompt, response)

    def build_prompt(self, messages):
        # messages: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == "user":
                prompt += f"<|user|>\n{content}\n"
            elif role == "assistant":
                prompt += f"<|assistant|>\n{content}\n"
        prompt += "<|assistant|>\n"
        return prompt

    def postprocess_response(self, prompt, full_response):
        return full_response[len(prompt):].strip()
