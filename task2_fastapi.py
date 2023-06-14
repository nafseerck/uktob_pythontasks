from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code if hasattr(exc, "status_code") else 500,
        content={"message": "Error", "detail": str(exc)},
    )

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    REQUEST_TIMEOUT = float(request.headers.get("X-TIMEOUT", 0))
    if REQUEST_TIMEOUT:
        try:
            start_time = time.time()
            return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT)
        except asyncio.TimeoutError:
            total_time = time.time() - start_time
            return JSONResponse(
                status_code=504,
                content={"message": "Timeout", "detail": f"Request time exceeded ({total_time} seconds)"}
            )
    else:
        return await call_next(request)

@app.get("/")
def root():
    return {
        "endpoints": [
            "/register",
            "/login",
        ],
        "error": ""
    }

@app.get("/test/timeout")
def test_timeout(sleep_time:int):
    time.sleep(sleep_time)
    return {
        "message": "ok"
    }

# User model
class User(BaseModel):
    username: str
    password: str

# In-memory storage for registered users (a dictionary)
users_db = {}

# User registration endpoint
@app.post("/register")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

# User login endpoint
@app.post("/login")
def login_user(user: User):
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Access denied")
    return {"message": "Access granted"}

