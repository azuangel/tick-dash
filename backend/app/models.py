from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Tick(BaseModel):
    timestamp: float
    price: float
    volume: float


class TickWithVWAP(Tick):
    vwap: float


class TickDB(SQLModel, table=True):
    __tablename__ = "ticks"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(index=True)
    price: float
    volume: float
