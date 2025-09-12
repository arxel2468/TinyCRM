import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet, apiPost, apiPatch } from "../utils/api";

const STAGES = ["new", "qualified", "won", "lost"];

export default function Deals() {
  const [items, setItems] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [min, setMin] = useState("");
  const [title, setTitle] = useState(""); const [amount, setAmount] = useState("");
  const [stage, setStage] = useState("new"); const [company, setCompany] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => { (async () => {
    const qs = min ? `?min_amount=${min}` : "";
    const data = await apiGet(`/api/deals/${qs}`);
    setItems(data.results || []);
  })(); }, [min]);

  useEffect(() => { (async () => {
    const data = await apiGet("/api/companies/");
    const list = data.results || [];
    setCompanies(list);
    if (!company && list.length) setCompany(list[0].id);
  })(); }, []);

  async function add(e) {
    e.preventDefault(); setErr("");
    try {
      await apiPost("/api/deals/", { title, amount, stage, company });
      setTitle(""); setAmount(""); setStage("new");
      const data = await apiGet("/api/deals/");
      setItems(data.results || []);
    } catch { setErr("Failed to add deal"); }
  }

  async function changeStage(id, s) {
    try {
      await apiPatch(`/api/deals/${id}/`, { stage: s });
      const data = await apiGet("/api/deals/");
      setItems(data.results || []);
    } catch { setErr("Failed to update stage"); }
  }

  async function exportCSV() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/exports/deals.csv`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "deals.csv"; a.click();
    URL.revokeObjectURL(url);
  } catch {
    setErr("Failed to export CSV");
  }
}
  return (
    <main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
      <Nav />
      <h2>Deals</h2>
      <button onClick={exportCSV} style={{ marginLeft: 8 }}>Export CSV</button>
      <div style={{ marginBottom: 12 }}>
        <input placeholder="min amount" value={min} onChange={(e) => setMin(e.target.value)} />
        <button onClick={() => { /* min triggers useEffect */ }}>Filter</button>
      </div>

      <form onSubmit={add} style={{ display: "grid", gap: 8, marginBottom: 16, maxWidth: 420 }}>
        <input placeholder="title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <input placeholder="amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
        <select value={stage} onChange={(e) => setStage(e.target.value)}>
          {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <select value={company} onChange={(e) => setCompany(e.target.value)}>
          {companies.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button type="submit">Add Deal</button>
      </form>

      {err && <p style={{ color: "red" }}>{err}</p>}
      <ul>
        {items.map((d) => (
          <li key={d.id}>
            {d.title} — ₹{d.amount} —{" "}
            <select value={d.stage} onChange={(e) => changeStage(d.id, e.target.value)}>
              {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </li>
        ))}
      </ul>
    </main>
  );
}