from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "fzm_2820da5f_l1tlflor"  # Frozen API key

# Search songs using FrozenMusic API
@app.get("/api/search")
def search(query: str):
    try:
        res = requests.get(
            f"https://frozenmusic.vercel.app/api/v1/search?query={query}",
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

# Get song details from saavn.dev API
@app.get("/api/song/{song_id}")
def get_song(song_id: str):
    try:
        res = requests.get(
            f"https://saavn.dev/api/songs/{song_id}",
            timeout=10
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}
