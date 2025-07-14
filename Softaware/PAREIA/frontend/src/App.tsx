import React, { useState } from 'react';
import Login from './Login';

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [nome, setNome] = useState<string>('');
  const [perfil, setPerfil] = useState<string>('');

  const handleLogin = (newToken: string, nome: string, perfil: string) => {
    setToken(newToken);
    setNome(nome);
    setPerfil(perfil);
  };

  return (
    <div>
      <h1>Painel PAREIA</h1>
      {!token ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          <p>Bem-vindo, {nome}!</p>
          <p>Perfil: {perfil}</p>
          <p>Token: {token.slice(0, 10)}...</p>
        </>
      )}
    </div>
  );
}

export default App;
