import os
import requests
import json

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    def generate(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate text using Groq API (single attempt)"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional marketing and sales AI assistant. Provide structured, actionable responses."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stream": False
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            print("Groq API Response:", result)  # debug
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError("No response from AI model")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def generate_with_retry(self, prompt, max_tokens=2000, temperature=0.7, retries=3):
        """Try to generate content multiple times if API fails"""
        for attempt in range(retries):
            try:
                return self.generate(prompt, max_tokens=max_tokens, temperature=temperature)
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
        raise Exception(f"All {retries} attempts to generate content failed")
