from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Payloads(Base):
    __tablename__ = "payloads"

    id = Column(Integer, primary_key=True, index=True)
    payload = Column(String)
