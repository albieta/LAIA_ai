from typing import Any, List
from services.llm.llm import call_llm
import json

async def task_to_perform(model: str, apikey: str, data: Any, query: str):

    complete_data = []
    context = { "role": "system", "content": """You have to analyse a conversation between a user and an assistant, and 
               determine wheather (1) the user's need is to define/create an openapi specs for an application (this case
               applies if the project is still not created), or (2) if the project is already created and changes need to be made
               in the code of the backend files, or (3) if the project is already created and changes need to be made in the frontend 
               files. You should only respond with this possible answers in json format (1) {"task": "openapi"} or (2) {"task": "backend"} 
               or (3) {"task": "frontend"} if you do not know, or have doubts where to classify it, respond {"task": "openapi"}""" }
    complete_data.append(context)

    for data_element in data:
        user_message = { "role": "user", "content": data_element["user"] }
        assistant_message = { "role": "assistant", "content": data_element["assistant"] }
        complete_data.append(user_message)
        complete_data.append(assistant_message)
    
    complete_data.append({ "role": "user", "content": query })

    response = ""
    counter_laia = 0
    
    while "{" not in response and "}" not in response and counter_laia <= 5:
        response, response_data = await call_llm(model=model, apikey=apikey, data=complete_data)
        
        response_json = response[response.find("{"):response.find("}")+1]

        try:
            response_json = json.loads(response_json)
            if "task" in response_json and response_json["task"] in ["openapi", "backend", "frontend"]:
                return response_json["task"]
        except ValueError:
            response_data.append({ "role": "user", "content": 'The format of the response was not correct, it should be either {"task": "openapi"} or {"task": "backend"} or {"task": "frontend"}' })
        
        counter_laia += 1

    return "openapi"
