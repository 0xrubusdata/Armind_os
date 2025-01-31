import "../styles/globals.css";
import Layout from "../components/templates/Layout";

export const metadata = {
  title: "Armind OS - AI-Driven Framework",
  description: "AI-powered agent for crypto trading",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}
