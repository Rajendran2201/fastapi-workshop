from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional

API_VERSION = "/api/v1"

class UserModel(BaseModel):
    username: str
    password: str

class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[str]

app = FastAPI()

db = {"users":[{"default":"default", "rajendran":"raj2201"}]}

@app.get(API_VERSION + "/user")
async def user():
    return db

@app.post(API_VERSION + "/user")
async def post_user(user: UserModel, status_code=201):
    username = user.username
    password = user.password
    db["users"].append({username:password})
    return {"message": "User created successfully"}

@app.get(API_VERSION + "/user/{username}")
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

@app.patch(API_VERSION + "/users", status_code=200)
async def update_user(user: UpdateUser):
    username = user.username
    new_password = user.password
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            user[username] = new_password
            break
    if found:
        return JSONResponse(
            content={"message": f"User: {username} has been updated successfully"},
                     status_code=200,
                     media_type="application/json")
    return JSONResponse(
            content={"message": f"User: {username} is not found in the DB"},
                     status_code=404,
                     media_type="application/json")


@app.delete(API_VERSION + "/users/{username}")
async def update_user(username: str):
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            db["users"].pop(db["users"].index(user))
            break
    if found:
        return JSONResponse(
            content={"message": f"User: {username} has been deleted successfully"},
                     status_code=200,
                     media_type="application/json")
    return JSONResponse(
            content={"message": f"User: {username} is not found in the DB"},
                     status_code=404,
                     media_type="application/json")