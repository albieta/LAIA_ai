import json
import os
from fastapi import APIRouter, HTTPException
from typing import List
from models.action import ActionModel

actions_routes_router = APIRouter()

async def action_exists(action_name: str) -> bool:
    file_path = f'actions/{action_name}.json'
    return os.path.exists(file_path)

async def write_action_to_file(action: ActionModel) -> None:
    file_path = f'actions/{action.name}.json'
    with open(file_path, 'w') as file:
        action_data = {
            "name": action.name,
            "description": action.description,
            "inputs": action.inputs,
            "code": action.code
        }
        json.dump(action_data, file, indent=4)

@actions_routes_router.post('/action/')
async def create_action(action: ActionModel):
    if await action_exists(action.name):
        raise HTTPException(status_code=400, detail="Action with this name already exists")
    await write_action_to_file(action)
    return {"message": "Action created successfully"}

@actions_routes_router.post('/action/search')
async def search_action(search_query: dict):
    # It receives the search query as input.
    # It returns a list of actions (name + description) which might be of use to perform such action
    # Examples of the input format --> 
    #       "I need to read a file"
    #       "I need to write the file with such name and add this code in it"

    pass

@actions_routes_router.get('/action/read/{action_name}')
async def read_action(action_name: str):
    # It returns the action with such name

    if not await action_exists(action_name):
        raise HTTPException(status_code=404, detail="Action not found")
    file_path = f'actions/{action_name}.json'
    with open(file_path, 'r') as file:
        action_data = json.load(file)
        return action_data

@actions_routes_router.get('/action/{action_name}')
async def run_action(action_name: str):
    # It runs the action with such name on the system

    if not await action_exists(action_name):
        raise HTTPException(status_code=404, detail="Action not found")
    file_path = f'actions/{action_name}.json'
    with open(file_path, 'r') as file:
        action_data = json.load(file)
        return ActionModel(**action_data)

@actions_routes_router.put('/action/{action_name}')
async def update_action(action_name: str, action: dict):
    # It updates an already existing function
    pass

@actions_routes_router.delete('/action/{action_name}')
async def delete_action(action_name: str):
    # It deletes an already existing function
    
    if not await action_exists(action_name):
        raise HTTPException(status_code=404, detail="Action not found")
    file_path = f'actions/{action_name}.json'
    os.remove(file_path)
    return {"message": "Action deleted successfully"}