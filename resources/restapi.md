
## 🔍 What is a REST API?

A **REST API** (REpresentational State Transfer API) is a way for two systems (like a frontend app and backend server) to communicate using **HTTP**.

It's commonly used to **create, read, update, and delete (CRUD)** data.

![](https://i.imgur.com/bxUbX2p.png)

---

## 📦 Core Concepts of REST API

|Method|Action|Example|
|---|---|---|
|`GET`|Read data|`/users` → list users|
|`POST`|Create new data|`/users` → add a user|
|`PUT`|Update entire data|`/users/1` → update user|
|`PATCH`|Update partial data|`/users/1` → edit username|
|`DELETE`|Delete data|`/users/1` → remove user|

---

## 🛠️ Example REST API (Users)

Let’s say we want to build an API to manage users using FastAPI:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

db = []

# GET: List all users
@app.get("/users")
def get_users():
    return db

# POST: Add a user
@app.post("/users")
def add_user(user: User):
    db.append(user)
    return {"message": "User added successfully"}

# GET: Get a specific user
@app.get("/users/{username}")
def get_user(username: str):
    for u in db:
        if u.username == username:
            return u
    raise HTTPException(status_code=404, detail="User not found")

# PUT: Replace a user
@app.put("/users/{username}")
def update_user(username: str, updated_user: User):
    for i, u in enumerate(db):
        if u.username == username:
            db[i] = updated_user
            return {"message": "User updated"}
    raise HTTPException(status_code=404, detail="User not found")

# DELETE: Delete a user
@app.delete("/users/{username}")
def delete_user(username: str):
    for i, u in enumerate(db):
        if u.username == username:
            del db[i]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
```

---
###  Why REST API is Useful

- Works with any frontend (React, Flutter, Android, etc.)
- Simple, human-readable structure
- You can test it using Bruno, Thunder Client, Postman, etc.
- Easy to version and maintain

---
## **REST vs. SOAP APIs**

**Related: [What is a SOAP API?](https://blog.postman.com/soap-api-definition/)**

There has always been a debate in the application programming interface (API) industry about [SOAP vs. REST](https://blog.postman.com/soap-vs-rest/). SOAP and REST are two different approaches for building APIs. SOAP is considered a protocol, while REST is considered a set of guidelines. REST allows for flexible API development using methods like JSON, URLs, and [HTTP](https://blog.postman.com/what-is-http/), while SOAP uses XML for sending data. To decide which architectural style is right for you, it is critical to know the good and the bad of building a proper design when planning for your next API.

**Simple Object Access Protocol (SOAP)** helps define messages exchanged between systems and used by applications. In contrast to REST, SOAP is an actual protocol that provides you with stricter detail about what an API does. Even though SOAP may not be a suitable choice for newer mobile developers, it provides a solid foundation for enterprise resources integrations. The main takeaway here is that SOAP provides a solid, reliable pattern you can use when you don’t require a more date-centric [API design](https://www.postman.com/api-platform/api-design/) pattern like REST.

**REpresentational State Transfer (REST)** is a software architectural style of delivering APIs dependent on the HTTP specification the web is built upon. REST APIs utilize the uniform resource locator (URL) to make data available using the web. This helps to ultimately maximize usage of [HTTP methods](https://blog.postman.com/what-are-http-methods/), headers, and other essential web building blocks. Unlike SOAP, REST is a common starting place for most teams when they begin investing in APIs because it provides a simple and widely recognized set of design patterns.

---
![](https://restfulapi.net/wp-content/uploads/What-is-REST.png)

