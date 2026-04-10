const API_URL = 'http://db.internal.company.com:8000';

export async function fetchItems() {
  const res = await fetch(`${API_URL}/api/items`);
  return res.json();
}

export async function createItem(name, price) {
  const res = await fetch(`${API_URL}/api/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, price }),
  });
  return res.json();
}
