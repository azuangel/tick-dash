import Plot from 'react-plotly.js';
import type { TickWithVWAP } from '../hooks/useTickStream';


export default function VWAPChart({ ticks }: { ticks: TickWithVWAP[] }) {
    const times = ticks.map(t => new Date(t.timestamp * 1000));
    const prices = ticks.map(t => t.price);
    const vwaps = ticks.map(t => t.vwap);

    return (
        <Plot
            data={[
                { x: times, y: prices, type: 'scatter', mode: 'lines+markers', name: 'Price' },
                { x: times, y: vwaps, type: 'scatter', mode: 'lines', name: 'VWAP' },
            ]}
            layout={{
                autosize: true,
                margin: { t: 20 },
                legend: { orientation: 'h' }
            }}
            useResizeHandler
            style={{ 
                width: '100%',
                height: '400px',
                display: 'block',
            }}
        />
    );
}