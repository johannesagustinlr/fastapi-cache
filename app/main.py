from fastapi import FastAPI, HTTPException, status
import redis
from app.schema import CreateInput


app = FastAPI()
rd = redis.Redis(host="localhost", port=6379, db=0)


@app.get("/")
def home():
    return "Initial Load"


@app.post("/payload")
def create_new_payload(payload: CreateInput):
    merging_element = []
    if len(payload.list_1) != len(payload.list_2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload length is not equal",
        )

    for element in zip(payload.list_1, payload.list_2):
        for item in element:
            merging_element.append(item.upper())

    print(merging_element)
