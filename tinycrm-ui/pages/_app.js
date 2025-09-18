import "@/styles/globals.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const qc = new QueryClient();

export default function App({ Component, pageProps }) {
  return <QueryClientProvider client={qc}><Component {...pageProps} /></QueryClientProvider>;
}
