const API_GATEWAY = import.meta.env.VITE_API_GATEWAY || 'http://localhost:8000';

export async function login(): Promise<string> {
  const response = await fetch(`${API_GATEWAY}/token`, {
    method: 'POST',
  });
  const data = await response.json();
  return data.access_token;
}

export async function getProtectedData(token: string): Promise<any> {
  const response = await fetch(`${API_GATEWAY}/users`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('Unauthorized or error fetching data');
  }
  return await response.json();
}
