from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crawler import get_bbc_news  # <- must match exactly

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news")
def fetch_news():
    return get_bbc_news()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}
