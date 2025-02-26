"use client"

import Link from "next/link"
import { Shield } from "lucide-react"
import { ButtonAbout } from "@/components/ui/button-about"

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Header */}
      <header className="border-b border-muted">
        <div className="flex h-16 items-center justify-between px-8">
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            <Link href="/" className="text-xl font-bold glow text-primary">
              GovWatch
            </Link>
          </div>
          <nav className="flex gap-6">
            <Link href="/">
              <ButtonAbout label="Home" />
            </Link>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1">
        <section className="hero-pattern border-b border-muted py-12">
          <div className="container mx-auto px-4">
            <h1 className="text-4xl font-bold text-center mb-8">About GovWatch</h1>
            
            <div className="max-w-3xl mx-auto bg-card rounded-lg shadow-sm p-8 space-y-6">
              {/* Mission Section */}
              <section>
                <h2 className="text-2xl font-bold mb-3">Our Mission</h2>
                <p className="text-muted-foreground">
                  GovWatch brings transparency to government spending through technology, making contract data accessible to everyone.
                </p>
              </section>

              {/* Philosophy Section */}
              <section>
                <h2 className="text-2xl font-bold mb-3">Our Philosophy</h2>
                <ul className="space-y-2 text-muted-foreground">
                  <li><span className="font-semibold">Transparency:</span> Making government spending visible to all citizens</li>
                  <li><span className="font-semibold">Accessibility:</span> Creating tools anyone can use, regardless of technical expertise</li>
                  <li><span className="font-semibold">Innovation:</span> Using AI to extract insights from complex data</li>
                </ul>
              </section>

              {/* Technology Approach */}
              <section>
                <h2 className="text-2xl font-bold mb-3">Our Technology</h2>
                <ul className="space-y-2 text-muted-foreground">
                  <li><span className="font-semibold">AI-Powered Search:</span> Vector embeddings and semantic search for natural language queries</li>
                  <li><span className="font-semibold">Automated Data Collection:</span> Regular scraping of defense contract data</li>
                  <li><span className="font-semibold">User-Friendly Interface:</span> Clean design that works on all devices</li>
                </ul>
              </section>

              {/* Future Vision */}
              <section>
                <h2 className="text-2xl font-bold mb-3">Our Vision</h2>
                <p className="text-muted-foreground">
                  We're expanding beyond DoD contracts to all government spending, creating a comprehensive platform 
                  that connects disparate data sources and enables citizens to engage more deeply with how their tax dollars are spent.
                </p>
              </section>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-muted py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} GovWatch. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
} 