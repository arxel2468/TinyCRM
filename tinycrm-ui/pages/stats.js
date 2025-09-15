import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet } from "../utils/api";
export default function Stats() {
const [data, setData] = useState(null);
const [days, setDays] = useState("30");
useEffect(() => { (async () => {
const res = await apiGet(/api/stats/deals/?days=${days});
setData(res);
})(); }, [days]);

return (
<main style={{ maxWidth: 720, margin: "20px auto", fontFamily: "system-ui" }}>
<Nav />
<h2>Deals Stats</h2>
<div>
<input value={days} onChange={(e) => setDays(e.target.value)} /> days
</div>
{!data ? <p>Loading…</p> : (
<>
<p>Total deals: {data.totals?.count || 0} | Total amount: ₹{data.totals?.amount || 0}</p>
<ul>
{data.by_stage?.map((row) => (
<li key={row.stage}>
{row.stage}: {row.count} deals — ₹{row.amount || 0}
</li>
))}
</ul>
</>
)}
</main>
);
}
