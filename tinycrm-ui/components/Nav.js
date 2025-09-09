import { clearToken } from "../utils/api";

export default function Nav() {
  return (
    <nav style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
      <a href="/contacts" style={{ marginRight: 12 }}>Contacts</a>
      <a href="/deals" style={{ marginRight: 12 }}>Deals</a>
      <button onClick={() => { clearToken(); window.location.href = "/login"; }}>
        Logout
      </button>
    </nav>
  );
}