from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Get YouTube API Key from Railway environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.get("/")
def home():
    return {"message": "Spotube backend is running!"}

@app.get("/trending")
def get_trending_videos():
    if not YOUTUBE_API_KEY:
        return {"error": "Missing YouTube API Key"}

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=IN&maxResults=10&key={YOUTUBE_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch trending videos"}
