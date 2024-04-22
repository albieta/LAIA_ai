from typing import Any, List
import requests
import openai

async def call_llm(model: str, apikey: str, data: List):
    try: 
        if model == "openai":
            openai.api_key = apikey
            text = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=data,
                temperature=1
            )
            response = text['choices'][0]['message']['content']

            data.append({"role": "assistant", "content": response})
        else:
            url = 'http://147.83.113.192:30147/ollama/api/chat'
        
            message_data = {
                "model": model,
                "messages": data,
                "stream": False
            }

            headers = {
                "Content-Type": "application/json"
            }

            response_llm = requests.post(url, json=message_data, headers=headers)
            response = response_llm.json()['message']['content']

            data.append({"role": "assistant", "content": response})

        return response, data
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")
