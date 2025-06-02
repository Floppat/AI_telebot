import requests
import config


class Ai():
    def __init__(self, messages: list) -> None:
        self.messages = messages

    def new_prompt(self, text):
        new = {
                    "role": "user",
                    "text": text
                }
        self.messages.append(new)
        #print(self.messages)
    
    def asis_ans(self, text):
        new = {
                    "role": "assistant",
                    "text": text
                }
        self.messages.append(new)
        #print(self.messages)
    
    def get_prompt(self):
        self.prompt = {
            "modelUri": f"gpt://{config.id_ya}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": "2000"
            },
            "messages": self.messages
        }
        return self.prompt
    
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
    
