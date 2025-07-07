from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/search")
def search_song(query: str = Query(..., description="Song name")):
    try:
        # Search on YouTube
        ydl_opts = {'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

            url = result['webpage_url']
            title = result['title']
            channel = result['uploader']
            thumbnail = result['thumbnail']

            # Get direct audio stream
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        return {
            "title": title,
            "channel": channel,
            "thumbnail": thumbnail,
            "audio_url": audio_url,
            "source_url": url,
        }

    except Exception as e:
        return {"error": str(e)}
