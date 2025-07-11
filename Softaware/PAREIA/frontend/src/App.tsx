import React, { useState } from 'react';
import { login, getProtectedData, predictML } from './api';

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [users, setUsers] = useState<any[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [feature1, setFeature1] = useState('');
  const [feature2, setFeature2] = useState('');
  const [prediction, setPrediction] = useState<number | null>(null);

  const handleLogin = async () => {
    try {
      const jwt = await login();
      setToken(jwt);
      setError(null);
    } catch (err) {
      setError('Failed to login');
    }
  };

  const fetchData = async () => {
    if (!token) return;
    try {
      const data = await getProtectedData(token);
      setUsers(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch protected data');
    }
  };

  const handlePredict = async () => {
    if (!token) return;
    try {
      const result = await predictML(token, parseFloat(feature1), parseFloat(feature2));
      setPrediction(result.prediction);
      setError(null);
    } catch (err) {
      setError('Failed to get prediction');
    }
  };

  return (
    <div className="App">
      <h1>Microservices Frontend</h1>
      {!token ? (
        <button onClick={handleLogin}>Login</button>
      ) : (
        <>
          <p>Token: {token.slice(0, 20)}...</p>
          <button onClick={fetchData}>Get Users</button>
        </>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {users && (
        <ul>
          {users.map((u, i) => (
            <li key={i}>{u.name}</li>
          ))}
        </ul>
      )}

      {token && (
        <div style={{ marginTop: 20 }}>
          <h2>ML Prediction</h2>
          <input
            type="number"
            placeholder="Feature 1"
            value={feature1}
            onChange={(e) => setFeature1(e.target.value)}
          />
          <input
            type="number"
            placeholder="Feature 2"
            value={feature2}
            onChange={(e) => setFeature2(e.target.value)}
          />
          <button onClick={handlePredict}>Predict</button>
          {prediction !== null && <p>Prediction: {prediction}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
