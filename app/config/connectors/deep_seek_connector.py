import requests
import os

class DeepSeekConnector:
    base_url = 'https://api.deepseek.com/'
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Chave não encontrada")
    def send_message(self, messages:list, max_tokens=200, temperature=0.7):
        headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }
    
        endpoint = f"{self.base_url}v1/chat/completions"  
        payload = {
        "model": "deepseek-chat",  # Modelo específico da DeepSeek
        "messages": messages,
        "max_tokens": max_tokens,  
        "temperature": temperature,  
    }

        response = requests.post(endpoint, headers=headers, json=payload)
    
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na requisição: {response.status_code}, {response.text}")