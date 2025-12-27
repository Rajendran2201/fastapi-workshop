from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional

API_VERSION = "/api/v1"

class UserModel(BaseModel):
    username: str
    password: str
    city: str

class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    city: Optional[str]

app = FastAPI()

db = {"users":[{"default": {"password":"default", "city":"Coimbatore"}},
               {"rajendran": {"password":"raj2201", "city":"Coimbatore"}},
               {"krishi": {"password":"krishu", "city":"Banglore"}},
               {"karthik": {"password":"karz", "city":"Hosur"}},
               {"user_2": {"password":"user_admin", "city":"Hosur"}},
               {"user_3": {"password":"user_admin", "city":"Hosur"}},
               {"user_1": {"password":"user_admin", "city":"Chennai"}},
               {"user_4": {"password":"user_admin", "city":"Hosur"}},
               {"user_5": {"password":"user_admin", "city":"Chennai"}},
    ]}


@app.get(API_VERSION + "/user")
async def user():
    return db

@app.post(API_VERSION + "/user")
async def post_user(user: UserModel, status_code=201):
    username = user.username
    password = user.password
    city = user.city
    db["users"].append({username: {"password":password, "city":city}})
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
            user[username]["password"] = new_password
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
async def delete_user_by_username(username: str):
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

@app.get(API_VERSION + "/filter")
async def filter_users(city: Optional[str], limit: Optional[int] = 3, offset: Optional[int] = 0):
    matching_users = []
    for user in db["users"]:
        username = list(user.keys())[0]
        user_city = list(user.values())[0].get("city")
        if user_city == city:
            matching_users.append(username)

    paginated_users = matching_users[offset:offset+limit]

    if paginated_users:
        return JSONResponse(
            content={
                "message": f"Users{f' in {city}' if city else ''}",
                "users": paginated_users
            },
            status_code=200,
            media_type="application/json"
        )
    return JSONResponse(
        content={"message": f"No users found{f' in {city}' if city else ''}"},
        status_code=404,
        media_type="application/json"
    )




