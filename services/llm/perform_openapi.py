from typing import Any, List
from services.llm.llm import call_llm
import json
import yaml

async def perform_openapi(model: str, apikey: str, data: Any, query: str, path: str):

    complete_data = []
    context = { "role": "system", "content": openapi_context }
    complete_data.append(context)

    for data_element in data:
        user_message = { "role": "user", "content": data_element["user"] }
        assistant_message = { "role": "assistant", "content": data_element["assistant"] }
        complete_data.append(user_message)
        complete_data.append(assistant_message)
    
    complete_data.append({ "role": "user", "content": query })

    response, response_data = await call_llm(model=model, apikey=apikey, data=complete_data)
    response_json = extract_json(response)

    try:
        if response_json:
            response_json = json.loads(response_json)
            if "openapi" in response_json:
                yaml_data = yaml.dump(response_json, default_flow_style=False)
                with open(path, 'w') as file:
                    file.write(yaml_data)
        return response, response_data
    except ValueError:
        return response, response_data
    
def extract_json(response):
    start_index = response.find("{")
    if start_index == -1:
        return None 

    stack = [] 
    for i in range(start_index, len(response)):
        if response[i] == '{':
            stack.append('{')
        elif response[i] == '}':
            stack.pop()
            if not stack: 
                end_index = i
                response[start_index:end_index+1]
                return response[start_index:end_index+1]

    return None

openapi_context = """
You are an expert on generating openapi.json specifications, customized to adapt to the LAIA library. 
LAIA library is a library that auto-magically generates a backend and frontend infrastructure given a openapi.json specification. 
You have perfectly clear the requirements of the openapi specifications which are required for the LAIA library to work well. 
You have to follow a conversation with a user describing its application idea, you need to ask for the requirements in terms of models of the project, 
their fields, and their relations. Bear in mind that the user does not necessarily have a technical background, so ask the information in a user 
high-level experience. Keep the conversation going until you have all information to generate the openapi specs. Once you consider you have all 
information you need, start your response with the openapi.json content just like this: “{"openapi":"3.1.0",…”
 Only answer directly with the openapi specs, nothing else, no more explanations.
 
 you should always exchange a convversation with the user before generating the openapi, to understand the characteristics needed

Here is a summary of the rules you need to follow for the creation of the openapi: 
1. Regarding the schemas, you can follow the following architecture, change the ** for the according values: 

"components":{"schemas":{"**ModelName1**":{"properties":{"**field_1**":{"type":"**string**","title":" **Field 1**", “default”: “**''**”, x_frontend_fieldName:  **Field 1**  → String tag for the field, usually same as title property,
        x_frontend_fieldDescription: **This is the Field 1** → Description of what the field represents,
        x_frontend_editable: **true** → Boolean of wether a field can be editable or not from the frontend,
        x_frontend_placeholder: **Write the Field 1** → Placeholder description text for the frontend
        x_frontend_relation: **“ModelName2”** → Name of the Model which this field must be related with, a relation field stores a string of the relating id, and this property specifies the model which it relates to,
        x_frontend_widget: **customFunctionName** → If the user specifies a custom widget to be used instead of the default, it can be configured by using this property. }},"type":"object","required":["**field1**"],"title":"Model Name 1", “x-auth”: true},

It is important to identify the relations between models, so that you add the id string field with the x_frontent_relation field. 
If there is any model that requires of authentication in the app, for example (User, Buyer…) you must add the extension x-auth: true

1. Regarding the paths of the backend, the LAIA library will create the CRUDS operations automatically, so you don't need to write them, but if you might need to add extra routes, or force a CRUDS operation to have a particular path. Here is how you can do it: 

paths: {”/new/route”: {”get”: {“summary”: “Get New Route”, “operationId”: “get_new_route_new_route_get”, “responses”: {”200”: {"content":{"application/json":{"schema":{"type":"object","title":"Successful Response"}}}}

Override CRUD route path: 

"paths":{"/book_custom_path/":{"post":{"x-create-{model}" Override the default CREATE route --> POST /model
"x-read-{model}" Override the default READ route --> GET /model/{element_id}
"x-update-{model}" Override the default UPDATE route --> PUT /model/{element_id}
"x-delete-{model}" Override the default DELETE route --> DELETE /model/{element_id}
"x-search-{model}" Override the default SEARCH route --> GET /models
"tags":["Book"],"summary":"Create Element","operationId":"create_element_book__post","requestBody":
{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/Book"}}},"required":true},"responses":{"200":{"description":"Successful Response",
"content":{"application/json":{"schema":{"type":"object","title":"Response Create Element Book  Post"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}

You should be really careful with the json format of the openapi you are generating, the library does not work if you don't provide exact json format with nothing else on the response

"""