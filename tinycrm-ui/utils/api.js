const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}
export function setToken(t) { if (typeof window !== "undefined") localStorage.setItem("token", t); }
export function clearToken() { if (typeof window !== "undefined") localStorage.removeItem("token"); }

async function handle(res) {
  if (res.status === 401 && typeof window !== "undefined") {
    clearToken(); window.location.href = "/login"; return;
  }
  if (!res.ok) throw new Error(await res.text());
  return res;
}

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { Authorization: `Bearer ${getToken()}` } });
  await handle(res);
  return res.json();
}
export async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${getToken()}` },
    body: JSON.stringify(body),
  });
  await handle(res);
  return res.json();
}
export async function apiPatch(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${getToken()}` },
    body: JSON.stringify(body),
  });
  await handle(res);
  return res.json();
}