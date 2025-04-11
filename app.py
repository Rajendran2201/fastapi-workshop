from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Your FastAPI server is running"}, 200

