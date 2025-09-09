const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}
export function setToken(t) {
  if (typeof window !== "undefined") localStorage.setItem("token", t);
}
export function clearToken() {
  if (typeof window !== "undefined") localStorage.removeItem("token");
}

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (res.status === 401 && typeof window !== "undefined") {
    clearToken();
    window.location.href = "/login";
    return;
  }
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify(body),
  });
  if (res.status === 401 && typeof window !== "undefined") {
    clearToken();
    window.location.href = "/login";
    return;
  }
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}