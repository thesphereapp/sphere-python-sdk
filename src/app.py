from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

from main.api.random.random_controller import random_router

app = FastAPI(title="Shpere server")

origins = [
    "https://thesphereapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
# random-router
api_router.include_router(random_router)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"Hello": "World"}
