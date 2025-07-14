import React, { useState } from 'react';

interface LoginResponse {
  access_token: string;
  nome: string;
  perfil: string;
}

export default function Login({ onLogin }: { onLogin: (token: string, nome: string, perfil: string) => void }) {
  const [login, setLogin] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro('');
    try {
      const res = await fetch(`${import.meta.env.VITE_API_GATEWAY}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ login, senha })
      });
      if (!res.ok) throw new Error('Login inválido');
      const data: LoginResponse = await res.json();
      onLogin(data.access_token, data.nome, data.perfil);
    } catch (err: any) {
      setErro(err.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <button type="submit">Entrar</button>
      </form>
      {erro && <p style={{ color: 'red' }}>{erro}</p>}
    </div>
  );
}
