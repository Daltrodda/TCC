import React, { useState } from 'react';
import { login, getProtectedData } from './api';

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [users, setUsers] = useState<any[] | null>(null);
  const [error, setError] = useState<string | null>(null);

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
    </div>
  );
}

export default App;
