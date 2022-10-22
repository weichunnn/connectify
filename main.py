from fastapi import FastAPI
from spotify import authenticate

app = FastAPI()


@app.get("/")
async def root():
  return authenticate()
