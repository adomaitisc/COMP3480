from fastapi import FastAPI, Cookie
from typing import Annotated
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

app = FastAPI()

# Default Route
@app.get("/")
async def root_route():
    return {"message": "Hello World!", "description": "This is the root route, it greets with 'Hello World!'"}

# Query Arguments
@app.get("/hello")
async def greet_route(name: str):
    return {"message": f"Hello {name}, how are you?", "description": "This route greets the user based on the name provided in the query parameters"}

# Path Arguments
@app.get("/sum/{one}/{two}")
async def sum_route(one: int, two: int):
    return {"sum": f"{one + two}", "description": "This route sums the first path argument with the second and returns the result"}

# Wikipedia Wrapper
@app.get("/wiki/{topic}")
async def redierct_wikipedia(topic: str):
    wiki_url = f"https://en.wikipedia.org/wiki/{topic}"
    return RedirectResponse(url=wiki_url)

@app.get("/weather")
async def get_weather(city: str = "Boston"):
    return { "city": city, "weather": "sunny", "description": "This route returns dummy weather data for the city given in query (default is Boston)." }

@app.get("/length/{text}")
async def get_length(text: str):
    return { "text": text, "length": len(text), "description": "This route returns the length of the path argument string." }

@app.get("/prime/{number}")
async def is_prime(number: int):
    desc = "This route returns wether the given nember is a prime number."
    if number < 2:
        return { "number": number, "is_prime": False, "description": desc }

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return { "number": number, "is_prime": False, "description": desc }

    return { "number": number, "is_prime": True, "description": "This route returns whether the given number is a prime number." }

# Auth methods
users = (("caua", 28),)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

class RegisterInput(BaseModel):
    name: str
    pin: int

# Post Route with Body
class LoginInput(BaseModel):
    name: str
    pin: int

@app.post("/register")
async def create_user(input: RegisterInput):
    global users
    if (input.name, input.pin) in users:
        return { "success": False }

    users += ((input.name, input.pin),)
    return {"success": True, "description": "This route creates a user at the user array.", "message": "Log in via /login now."}

@app.post("/login")
async def authenticate(input: LoginInput):
    global users
    if (input.name, input.pin) in users:
        return {"success": True, "description": "This route authenticates a user against the user array.", "token": auth_token}

    return {"success": False}

@app.get("/users")
async def list_users(token: Annotated[str | None, Cookie()] = None):
    if token == auth_token:
        return { "success": True, "users": [name for name, _ in users], "description": "This route checks if the user is authenticated, then returns the users in a list" }
    return { "success": False, "users": None }
