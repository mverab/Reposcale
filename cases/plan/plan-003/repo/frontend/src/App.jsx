import React, { useState, useEffect } from 'react';
import { fetchItems } from './api';

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems().then(setItems);
  }, []);

  return (
    <div>
      <h1>Platform</h1>
      <ul>
        {items.map(item => (
          <li key={item.id}>{item.name} — ${item.price}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
