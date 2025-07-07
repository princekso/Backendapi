from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import requests

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/search")
def search_song(query: str = Query(..., description="Song name to search")):
    try:
        # Step 1: Search song using YouTube API (unofficial)
        res = requests.get(f"https://ytsearch-api.vercel.app/api/search?q={query}").json()
        first_result = res["data"]["videos"][0]
        url = f"https://www.youtube.com/watch?v={first_result['videoId']}"

        # Step 2: Get direct audio link using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'skip_download': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        return {
            "title": first_result["title"],
            "channel": first_result["channel"],
            "thumbnail": first_result["thumbnail"],
            "audio_url": audio_url,
            "source_url": url,
        }

    except Exception as e:
        return {"error": str(e)}
