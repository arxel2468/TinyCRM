import Link from "next/link";
import { clearToken } from "../utils/api";

export default function Nav() {
  return (
    <nav style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
      <Link href="/contacts" style={{ marginRight: 12 }}>Contacts</Link>
      <Link href="/companies" style={{ marginRight: 12 }}>Companies</Link>{/* add this */}
      <Link href="/deals" style={{ marginRight: 12 }}>Deals</Link>
      <Link href="/stats" style={{ marginRight: 12 }}>Stats</Link>
      <button onClick={() => { clearToken(); window.location.href = "/login"; }}>
        Logout
      </button>
    </nav>
  );
}
