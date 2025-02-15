from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

YT_API_KEY = os.getenv("YT_API_KEY")
if not YT_API_KEY:
    raise ValueError("Missing YT_API_KEY")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/search"

@app.get("/videos")
async def search_videos(q: str = Query(..., description="Search query")):
    url = f"{YOUTUBE_API_BASE_URL}?part=snippet&type=video&q={q}&maxResults=10&key={YT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        videos = [
            {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "video_id": item["id"]["videoId"],
                "video_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in data.get("items", [])
            if "videoId" in item.get("id", {})
        ]
        return {"videos": videos}

    except requests.exceptions.RequestException as e:
        return JSONResponse(content={"error": f"Error fetching videos: {str(e)}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {str(e)}"}, status_code=500)

@app.get("/trending")
async def get_trending_videos():
    url = f"{YOUTUBE_API_BASE_URL}?part=snippet&type=video&chart=mostPopular&maxResults=10&key={YT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return JSONResponse(content={"error": f"Error fetching trending videos: {str(e)}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {str(e)}"}, status_code=500)

@app.get("/")
async def root():
    return {"message": "Hello! API is running."}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
