from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class UserModel(BaseModel):
    username: str
    password: str

app = FastAPI()

db = {"users":[{"default":"default", "rajendran":"raj2201"}]}

@app.get("/user")
async def user():
    return db

@app.post("/user")
async def post_user(user: UserModel, status_code=201):
    username = user.username
    password = user.password
    db["users"].append({username:password})
    return {"message": "User created successfully"}

@app.get("/user/{username}")
async def get_user_by_username(username:str):
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            break
    if found:
        return JSONResponse(
            content={"message": f"User: {username} is found in the DB"},
                     status_code=200,
                     media_type="application/json")
    return JSONResponse(
            content={"message": f"User: {username} is not found"},
                     status_code=404,
                     media_type="application/json")