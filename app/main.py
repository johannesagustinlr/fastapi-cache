from fastapi import FastAPI, HTTPException, status, Depends
import redis
from app.schema import CreateInput
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Payloads

app = FastAPI()
rd = redis.Redis(host="localhost", port=6379, db=0)


@app.get("/")
def home():
    return "Initial Load"


@app.post("/payload")
def create_new_payload(
    payloads: CreateInput,
    db: Session = Depends(
        get_db,
    ),
):
    interleaving_list = []
    if len(payloads.list_1) != len(payloads.list_2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload length is not equal",
        )

    for element in zip(payloads.list_1, payloads.list_2):
        for item in element:
            interleaving_list.append(item.upper())
    output = ", ".join(interleaving_list)

    payloads_data = Payloads(payload=output)

    db.add(payloads_data)
    db.commit()
    db.refresh(payloads_data)
    return {"output": payloads_data}
