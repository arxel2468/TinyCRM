import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet } from "../utils/api";

export default function Deals() {
  const [items, setItems] = useState([]);
  const [min, setMin] = useState("");
  const [err, setErr] = useState(null);

  useEffect(() => {
    (async () => {
      const qs = min ? `?min_amount=${min}` : "";
      const data = await apiGet(`/api/deals/${qs}`);
      setItems(data.results || []);
    })();
  }, [min]);

  async function importCSV(file) {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/imports/contacts/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      body: fd,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  return (
    <main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
      <Nav />
      <h2>Deals</h2>
      <div style={{ margin: "12px 0" }}>
  <label style={{ marginRight: 8 }}>Import Contacts (CSV)</label>
  <input type="file" accept=".csv,text/csv" onChange={async (e) => {
    if (!e.target.files?.length) return;
    try {
      const res = await importCSV(e.target.files[0]);
      alert(`Imported: ${res.created} created, ${res.updated} updated, ${res.skipped} skipped`);
      // Reload list
      const data = await apiGet(`/api/contacts/?search=${encodeURIComponent(q)}`);
      setItems(data.results || []);
    } catch (err) {
      setErr("Import failed");
    } finally {
      e.target.value = "";
    }
  }} />
</div>
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
