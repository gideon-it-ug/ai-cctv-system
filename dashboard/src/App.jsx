import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_ROOT = 'http://192.168.1.4:8000/api';

function App() {
  const [events, setEvents] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [eventsRes, camerasRes] = await Promise.all([
        axios.get(`${API_ROOT}/events/`),
        axios.get(`${API_ROOT}/cameras/`),
      ]);
      setEvents(eventsRes.data.results || eventsRes.data);
      setCameras(camerasRes.data.results || camerasRes.data);
      setError(null);
    } catch (err) {
      setError('Backend unreachable');
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  const todayCount = events.filter(e =>
    new Date(e.timestamp).toDateString() === new Date().toDateString()
  ).length;

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-dot" />
          SENTRY<span className="brand-accent">CV</span>
        </div>

        <div className="sidebar-section-label">Cameras</div>
        {cameras.length === 0 && <div className="empty-hint">No cameras registered yet</div>}
        {cameras.map((cam) => (
          <div className="camera-row" key={cam.id}>
            <span className={`status-dot ${cam.online ? 'online' : 'offline'}`} />
            <span className="camera-name">{cam.name}</span>
            <span className="camera-state">{cam.online ? 'LIVE' : 'OFFLINE'}</span>
          </div>
        ))}

        <div className="sidebar-section-label">Today</div>
        <div className="stat-block">
          <div className="stat-value">{todayCount}</div>
          <div className="stat-label">detections</div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <h1>Event Feed</h1>
          {error && <span className="error-pill">{error}</span>}
        </header>

        <div className="event-list">
          {events.length === 0 && (
            <div className="empty-state">No events yet. Monitoring will populate this feed.</div>
          )}
          {events.map((event) => (
            <div className="event-row" key={event.id}>
              {event.image && <img className="event-thumb" src={event.image} alt="" />}
              <div className="event-info">
                <div className="event-title">
                  <span className="event-type">{event.event_type.toUpperCase()}</span>
                  {event.camera_name}
                </div>
                <div className="event-meta">
                  <span className="confidence">{(event.confidence * 100).toFixed(0)}% confidence</span>
                  <span className="timestamp">{new Date(event.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;