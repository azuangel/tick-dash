from pydantic import BaseModel


class Tick(BaseModel):
    timestamp: float
    price: float
    volume: float


class TickWithVWAP(Tick):
    vwap: float
