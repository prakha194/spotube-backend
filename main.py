from fastapi import FastAPI
import requests
import os
from googleapiclient.discovery import build

app = FastAPI()

YT_API_KEY = os.getenv("YT_API_KEY")
if not YT_API_KEY:
    raise ValueError("Missing YT_API_KEY")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/videos"

@app.get("/videos")
async def search_videos(q: str):
    url = f"{YOUTUBE_API_BASE_URL}?part=snippet&q={q}&maxResults=10&key={YT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        videos = []
        for item in data.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'video_id': item['id']['videoId'],
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video)
        return {"videos": videos}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}, response.status_code if hasattr(response, 'status_code') else 500
    except Exception as e:
        return {"error": f"Error: {e}"}, 500

@app.get("/trending")
async def get_trending_videos():
    url = f"{YOUTUBE_API_BASE_URL}?part=snippet&chart=mostPopular&maxResults=10&key={YT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}, response.status_code if hasattr(response, 'status_code') else 500
    except Exception as e:
        return {"error": f"Error: {e}"}, 500

@app.get("/")
async def root():
    return {"message": "Hello!"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app=app, host="0.0.0.0", port=port)
