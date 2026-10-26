import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from '@/components/theme-provider';

export const metadata: Metadata = {
  title: 'ModelOps Lab',
  description: 'MLOps platform foundation and dashboard shell',
};

const STORAGE_KEY = 'modelops-theme';

const themeScript = `
  (function() {
    try {
      const savedTheme = localStorage.getItem('${STORAGE_KEY}');
      const preferredDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = savedTheme === 'light' || savedTheme === 'dark'
        ? savedTheme
        : (preferredDark ? 'dark' : 'light');

      document.documentElement.classList.toggle('dark', theme === 'dark');
      document.documentElement.style.colorScheme = theme;
    } catch (error) {
      document.documentElement.classList.remove('dark');
      document.documentElement.style.colorScheme = 'light';
    }
  })();
`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // The theme script mutates the root element before hydration, so this is the minimal scoped hydration suppression.
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
