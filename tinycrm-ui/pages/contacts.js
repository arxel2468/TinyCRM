import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet, apiPost } from "../utils/api";

export default function Contacts() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [q, setQ] = useState("");
  const [err, setErr] = useState("");

  async function load(query = "") {
    try {
      const data = await apiGet(`/api/contacts/?search=${encodeURIComponent(query)}`);
      setItems(data.results || []);
    } catch (e) {
      setErr("Failed to load contacts");
    }
  }

  useEffect(() => { load(); }, []);

  async function add(e) {
    e.preventDefault();
    setErr("");
    try {
      await apiPost("/api/contacts/", { name, email });
      setName(""); setEmail("");
      load(q);
    } catch {
      setErr("Failed to add contact");
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
      <Nav />
      <h2>Contacts</h2>

      <form onSubmit={add} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input placeholder="name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <button type="submit">Add</button>
      </form>

      <div style={{ margin: "8px 0" }}>
        <input placeholder="search" value={q} onChange={(e) => setQ(e.target.value)} />
        <button onClick={() => load(q)}>Search</button>
      </div>

      {err && <p style={{ color: "red" }}>{err}</p>}
      <ul>
        {items.map((c) => <li key={c.id}>{c.name} — {c.email}</li>)}
      </ul>
    </main>
  );
}