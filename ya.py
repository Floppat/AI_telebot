import requests
import config


class Ai():
    def __init__(self, messages: list) -> None:
        self.messages = messages

    def new_prompt(self, text):
        self.messages.append({"role": "user", "text": text})

    def asis_ans(self, text):
        self.messages.append({"role": "assistant", "text": text})

    def get_history(self):
        return self.messages
    
    def gpt(self):
        self.prompt = {
            "modelUri": f"gpt://{config.id_ya}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": "2000"
            },
            "messages": self.messages
        }
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {config.key_ya}"
        }
        
        response = requests.post(url, headers=headers, json=self.prompt)
        result = response.json().get('result')
        return result['alternatives'][0]['message']['text']
