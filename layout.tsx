export const metadata = {
  title: 'SHUBAAD',
  description: 'AI environmental resilience intelligence platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
