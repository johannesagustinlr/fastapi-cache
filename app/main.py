from fastapi import FastAPI
import redis

app = FastAPI()
rd = redis.Redis(host="localhost", port=6379, db=0)


@app.get("/")
def home():
    return "Initial Load"
