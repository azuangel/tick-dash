import { useTickStream } from './hooks/useTickStream'
import VWAPChart from './components/VWAPChart'
import './App.css'

export default function App() {
  const { ticks, sendTick } = useTickStream();

  const pushRandom = () => {
    const now = Date.now() / 1000;
    sendTick({ 
      timestamp: now,
      price: 100 + Math.random() * 10,
      volume: 10 + Math.random() * 5,
    });
  };

  return (
    <>
      <button className="btn-row" onClick={pushRandom}>Send random tick</button>
      <div style={{ width: '100%', maxWidth: 900, margin: '2rem auto' }}>
        <VWAPChart ticks={ticks} />
      </div>
      
    </>
  )
}