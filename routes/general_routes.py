from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from services.llm.task_to_perform import task_to_perform
from services.llm.perform_openapi import perform_openapi
from services.llm.perform_backend import perform_backend
from services.llm.perform_frontend import perform_frontend

general_routes_router = APIRouter()

class MessageRequest(BaseModel):
    data: List
    query: str
    path: str
    apikey: str

@general_routes_router.post('/chatmessage/{model}')
async def laia_message(model: str, message: MessageRequest):
    try: 
        task = await task_to_perform(model, message.apikey, message.data, message.query)

        response = ""
        response_data = ""

        if task == "openapi":
            response, response_data = await perform_openapi(model, message.apikey, message.data, message.query, message.path)
        elif task == "backend":
            response, response_data = await perform_backend(model, message.apikey, message.data, message.query)
        elif task == "frontend":
            response, response_data = await perform_frontend(model, message.apikey, message.data, message.query)

        return { 
            "response": response,
            "response_data": response_data 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
