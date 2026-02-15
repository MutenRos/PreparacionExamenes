import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { defaultMetadata } from "@/lib/seo";
import { NotificationProvider } from "@/contexts/NotificationContext";
import { AuthProvider } from "@/components/providers/AuthProvider";
import NotificationToast from "@/components/notifications/NotificationToast";
import SupportWidget from "@/components/SupportWidget";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = defaultMetadata;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <AuthProvider>
          <NotificationProvider>
            {children}
            <NotificationToast />
          </NotificationProvider>
          <SupportWidget />
        </AuthProvider>
      </body>
    </html>
  );
}
