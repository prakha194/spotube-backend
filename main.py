import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Get API key from environment variable

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY is not set in the environment")

# Your existing FastAPI code using YOUTUBE_API_KEY
