from typing import List
from fastapi import FastAPI, Request
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
            "/sum",
            "/concatenate",
        ],
        "error": ""
    }

@app.get("/test/timeout")
def test_timeout(sleep_time:int):
    time.sleep(sleep_time)
    return {
        "message": "ok"
    }

class NumbersRequest(BaseModel):
    numbers: List[int]

class ConcatenateRequest(BaseModel):
    string1: str
    string2: str

@app.post('/sum',tags=['Sum'], description='Sum of numbers')
def calculate_sum(numbers_request: NumbersRequest):
    try:
        numbers = numbers_request.numbers
        result = sum(numbers)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.post('/concatenate',tags=['Concatenate'], description='Concatenate Strings')
def concatenate_strings(concatenate_request: ConcatenateRequest):
    try:
        string1 = concatenate_request.string1
        string2 = concatenate_request.string2
        result = string1 + string2
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
