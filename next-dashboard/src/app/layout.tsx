import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Amul Sales Dashboard",
  description: "Field sales performance at a glance",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
