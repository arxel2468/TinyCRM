import { useState } from "react";
import { setToken } from "../utils/api";

export default function Login() {
  const [username, setU] = useState("");
  const [password, setP] = useState("");
  const [err, setErr] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) throw new Error("Invalid credentials");
      const data = await res.json();
      setToken(data.access);
      window.location.href = "/contacts";
    } catch (e) {
      setErr(e.message || "Login failed");
    }
  }

  return (
    <main style={{ maxWidth: 360, margin: "80px auto", fontFamily: "system-ui" }}>
      <h2>Login</h2>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 8 }}>
        <input placeholder="username" value={username} onChange={(e) => setU(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={(e) => setP(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      {err && <p style={{ color: "red" }}>{err}</p>}
    </main>
  );
}