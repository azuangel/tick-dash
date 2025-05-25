import { useEffect, useRef, useState } from 'react';


export interface TickWithVWAP {
    timestamp: number;
    price: number;
    volume: number;
    vwap: number;
}

export function useTickStream() {
    const [ticks, setTicks] = useState<TickWithVWAP[]>([])
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws/ticks');
        wsRef.current = ws;

        ws.onmessage = (evt) => {
            const tick = JSON.parse(evt.data) as TickWithVWAP;
            setTicks((prev) => [...prev.slice(-99), tick]);
        };
        return () => ws.close();
    }, []);

    return {
        ticks,
        sendTick: (t: Omit<TickWithVWAP, 'vwap'>) =>
            wsRef.current?.send(JSON.stringify(t)),
    };
}