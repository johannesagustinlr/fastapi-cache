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

    # Check if the list in payload is equal
    if len(payloads.list_1) != len(payloads.list_2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload length is not equal",
        )
    # Interleaving the both list
    for element in zip(payloads.list_1, payloads.list_2):
        for item in element:
            interleaving_list.append(item.upper())

    # Join the list into single string
    output = ", ".join(interleaving_list)

    # Insert data to database
    payloads_data = Payloads(payload=output)
    db.add(payloads_data)
    db.commit()
    db.refresh(payloads_data)

    # Put the payload to redis after created, expired in 100 secs
    rd.set(payloads_data.id, payloads_data.payload)
    rd.expire(payloads_data.id, 100)
    return {payloads_data}


@app.get("/payload/{id}")
def get_payload(
    id: int,
    db: Session = Depends(
        get_db,
    ),
):
    payload_to_return = rd.get(id)

    # Check if data in cache
    if not payload_to_return:
        # Get data from database
        payload_data = db.query(Payloads).filter(Payloads.id == id).first()
        if not payload_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data with id = {id} was not found",
            )
        # Save extracted in cache
        payload_to_return = payload_data.payload
        rd.set(id, payload_to_return)
        rd.expire(id, 100)

    result = {
        "output": payload_to_return,
    }

    return result
