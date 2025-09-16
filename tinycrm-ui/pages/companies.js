import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet, apiPost } from "../utils/api";

export default function Companies() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [website, setWebsite] = useState("");
  const [err, setErr] = useState("");

  async function load() {
    try {
      const data = await apiGet("/api/companies/");
      setItems(data.results || []);
    } catch {
      setErr("Failed to load companies");
    }
  }
  useEffect(() => { load(); }, []);

  async function add(e) {
    e.preventDefault();
    setErr("");
    try {
      await apiPost("/api/companies/", { name, website });
      setName(""); setWebsite("");
      load();
    } catch {
      setErr("Failed to add company");
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
      <Nav />
      <h2>Companies</h2>
      <form onSubmit={add} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input placeholder="name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="website (optional)" value={website} onChange={(e) => setWebsite(e.target.value)} />
        <button type="submit">Add</button>
      </form>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <ul>{items.map((c) => <li key={c.id}>{c.name} {c.website && `— ${c.website}`}</li>)}</ul>
    </main>
  );
}
