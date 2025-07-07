from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "fzm_2b4ecd31_jz2efhnt"

@app.get("/api/search")
def search(query: str):
    try:
        res = requests.get(
            f"https://frozenmusic.vercel.app/api/v1/search?query={query}",
            headers={"X-API-Key": API_KEY}
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}
