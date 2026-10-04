import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Odyssey - Multi-Agent Travel Planner",
  description:
    "Describe your trip in plain words and Odyssey's AI agents find flights, hotels and activities, check your budget and build your day-by-day itinerary.",
};

export const viewport: Viewport = {
  themeColor: "#0F766E",
};

// Fonts (Bungee + Rubik) and the light/dark theme are handled inside page.tsx,
// so the layout stays minimal.
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}