##  What is FastAPI?

**FastAPI** is a **modern, high-performance** web framework for building APIs with **Python 3.7+**. It’s designed to be **fast, easy to use**, and **developer-friendly**, especially for building **RESTful APIs** and **microservices**.

> ⚡ It’s called _Fast_ API not just for its speed, but also because it helps you write code faster with less effort.

---
## Create a basic API call

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}"}
```

To run this, execute the following command using uvicorn: 

`uvicorn app:app --reload`

---

## Creating a model using pydantic


```python
from fastapi import FastAPI

from pydantic import BaseModel

class UserModel(BaseModel):

	username: str
	
	password: str


app = FastAPI()

db ={"users":[]}


@app.get("/user")

async def user():

	return {"message": "Your FastAPI server is running"}, 200

  
@app.post("/user")

async def post_user(user: UserModel):

	username = user.username
	
	password = user.password
	
	db["users"].append({username:password})
	
	return {"message": "User created successfully"}, 200
```

## API Testing using Bruno

Let's try testing this API created now using `bruno`. Instead we can also use a VS Code extension called `thunder client`.

Bruno is an open-source API client built for developers. It’s:
- Local-first (no cloud storage)
- Version-control friendly (stores everything in your repo)
- Lightweight and privacy-respecting
### 🛠️ Steps to Use Bruno

#### 1. **Download & Install Bruno**

- Go to: [https://usebruno.com/download](https://usebruno.com/download)
- Choose your platform: **Windows**, **macOS**, or **Linux**
- Install it like any other desktop app
    
---

#### 2. **Create a Collection**

- Open Bruno
- Click `New Collection`
- Give it a name and choose a **directory** (folder) where Bruno will save the requests
    
> 💡 Every collection is stored as `.bruno` files in your local directory. This makes them easy to version control with Git.

---

#### 3. ➕ **Add Your First API Request**

- Click on the `+` icon to add a new request
- Choose method (`GET`, `POST`, etc.)
- Enter the API URL (e.g., `http://localhost:8000/user`)
- Add headers, query params, or body (for `POST`, `PUT`, etc.)
    

---

#### 4.  **Send the Request**

- Click the `Send` button
- You’ll see the response in the bottom panel (status code, headers, and JSON/body)
---


![](https://i.imgur.com/bPeyhw5.png)

---

### Searching for a user in the DB

Let's try creating a method to search for a user in the DB using their username. 

```python
@app.get("/user/{username}")

async def get_user_by_username(username:str):

	found = False
	
	for user in db["users"]:
		if user.get(username):
			found = True
			break
		
	if found:
		return {"message": f"User: {username} is found in the db"}, 200
	
	return {"message": f"User: {username} is not found"}, 404
```

![](https://i.imgur.com/mc0ykpL.png)

When we try to search for a user present in the DB, we will get the success message.

![](https://i.imgur.com/a7mLOBF.png)


But, when we try to fetch a user who is not present in the DB, we'll get the error message.

![](https://i.imgur.com/Uxs7wyf.png)

---
### Let's try using JSONResponse
![[Screenshot 2025-04-11 at 12.19.32.png]]
```python
from fastapi import FastAPI, HTTPException
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
async def post_user(user: UserModel):
    db["users"].append({user.username: user.password})
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)

@app.get("/user/{username}")
async def get_user_by_username(username: str):
    for user in db["users"]:
        if username in user:
            return JSONResponse(
                content={"message": f"User: {username} is found in the DB"},
                status_code=200
            )
    return JSONResponse(
        content={"message": f"User: {username} is not found"},
        status_code=404
    )

```


<!--⚠️Imgur upload failed, check dev console-->
