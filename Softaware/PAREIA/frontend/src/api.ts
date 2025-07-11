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

export async function predictML(token: string, feature1: number, feature2: number): Promise<any> {
  const response = await fetch(`${API_GATEWAY}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ feature1, feature2 }),
  });
  if (!response.ok) {
    throw new Error('Prediction failed');
  }
  return await response.json();
}
