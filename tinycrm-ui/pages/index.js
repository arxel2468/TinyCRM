import { useEffect } from "react";
import { getToken } from "../utils/api";

export default function Home() {
  useEffect(() => {
    if (getToken()) window.location.href = "/contacts";
    else window.location.href = "/login";
  }, []);
  return null;
}
