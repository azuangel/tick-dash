from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from collections import deque
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from .db import AsyncSessionLocal, init_db
from .models import Tick, TickWithVWAP, TickDB

app = FastAPI()

ROLLING_WINDOW = 100  # keep last 100 ticks only
ticks: deque[Tick] = deque(maxlen=ROLLING_WINDOW)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@app.websocket("/ws/ticks")
async def ticks_ws(ws: WebSocket, session: AsyncSession = Depends(get_session)):
    """
    Client sends ticks and vwap is calculated and returned through the Websocket.
    Stores Ticks on Postgress for historical data
    """
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            tick_in = Tick(**data)
            ticks.append(tick_in)

            # Store tick in db
            db_tick = TickDB(
                timestamp=datetime.fromtimestamp(tick_in.timestamp),
                price=tick_in.price,
                volume=tick_in.volume,
            )

            session.add(db_tick)
            await session.commit()

            # VWAP on the current rolling window
            total_vol = sum(t.volume for t in ticks)
            total_pv = sum(t.price * t.volume for t in ticks)
            vwap = total_pv / total_vol if total_vol else tick_in.price

            # Send tick with vwap to dashboard
            await ws.send_json(
                TickWithVWAP(**tick_in.model_dump(), vwap=vwap).model_dump()
            )
    except ValidationError as e:
        await ws.send_json({"error": e.errors()})
    except WebSocketDisconnect:
        pass
