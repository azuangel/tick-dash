from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from .models import Tick, TickWithVWAP
from collections import deque

app = FastAPI()

ROLLING_WINDOW = 100  # keep last 100 ticks only
ticks: deque[Tick] = deque(maxlen=ROLLING_WINDOW)


@app.websocket("/ws/ticks")
async def ticks_ws(ws: WebSocket):
    """
    Client sends ticks and vwap is calculated and returned through the Websocket
    """
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            tick = Tick(**data)
            ticks.append(tick)

            # VWAP on the current rolling window
            total_vol = sum(t.volume for t in ticks)
            total_pv = sum(t.price * t.volume for t in ticks)
            vwap = total_pv / total_vol if total_vol else tick.price

            await ws.send_json(
                TickWithVWAP(**tick.model_dump(), vwap=vwap).model_dump()
            )
    except ValidationError as e:
        await ws.send_json({"error": e.errors()})
    except WebSocketDisconnect:
        pass
