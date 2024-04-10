from fastapi import FastAPI
from routes.general_routes import general_routes_router
from routes.actions_routes import actions_routes_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_routes_router)
app.include_router(actions_routes_router)