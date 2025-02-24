import type React from "react"
import "@/app/globals.css"
import { Inter, Instrument_Serif } from "next/font/google"

const inter = Inter({ subsets: ["latin"] })
const instrumentSerif = Instrument_Serif({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-instrument-serif",
})

export const metadata = {
  title: "GovWatch - DoD Contract Search",
  description: "Search and analyze Department of Defense contract spending data using natural language queries",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} ${instrumentSerif.variable}`}>{children}</body>
    </html>
  )
}

