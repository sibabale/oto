import "./globals.css";

export const metadata = {
  title: "OTO Research + Trade",
  description: "Open-source starter for 5Y company research and paper trading"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
