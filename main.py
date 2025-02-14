@app.get("/test")
async def test():
    return {"message": "Hello from the backend!"}
