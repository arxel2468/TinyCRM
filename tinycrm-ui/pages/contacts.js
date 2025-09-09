import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet } from "../utils/api";

export default function Deals() {
  const [items, setItems] = useState([]);
  const [min, setMin] = useState("");

  useEffect(() => {
    (async () => {
      const qs = min ? `?min_amount=${min}` : "";
      const data = await apiGet(`/api/deals/${qs}`);
      setItems(data.results || []);
    })();
  }, [min]);

  return (
    <main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
      <Nav />
      <h2>Deals</h2>
      <div>
        <input placeholder="min amount" value={min} onChange={(e) => setMin(e.target.value)} />
        <button onClick={() => { /* triggers useEffect via min state */ }}>Filter</button>
      </div>
      <ul>
        {items.map((d) => <li key={d.id}>{d.title} — ₹{d.amount} — {d.stage}</li>)}
      </ul>
    </main>
  );
}