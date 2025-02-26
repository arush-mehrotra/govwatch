"use client"

import Link from "next/link"
import { Shield } from "lucide-react"
import { ButtonAbout } from "@/components/ui/button-about"

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background hero-pattern">
      {/* Header */}
      <header className="border-b border-muted">
        <div className="mx-auto w-full max-w-[800px] px-4 sm:px-6 lg:px-8 flex h-16 items-center justify-between">
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
        <section className="py-16">
          <div className="mx-auto w-full max-w-[800px] px-4 sm:px-6 lg:px-8">
            <h1 className="heading-serif mb-8 text-center text-5xl font-normal text-primary">
              About GovWatch
            </h1>
            
            <div className="mx-auto bg-secondary/30 rounded-2xl border border-muted shadow-md card-glow p-8 space-y-8">
              {/* Mission Section */}
              <section>
                <h2 className="text-2xl font-bold mb-3 text-primary">Our Mission</h2>
                <p className="text-muted-foreground">
                  GovWatch brings transparency to government spending through technology, making contract data accessible to everyone.
                </p>
              </section>

              {/* Philosophy Section */}
              <section>
                <h2 className="text-2xl font-bold mb-3 text-primary">Our Philosophy</h2>
                <ul className="space-y-2 text-muted-foreground">
                  <li><span className="font-semibold text-foreground">Transparency:</span> Making government spending visible to all citizens</li>
                  <li><span className="font-semibold text-foreground">Accessibility:</span> Creating tools anyone can use, regardless of technical expertise</li>
                  <li><span className="font-semibold text-foreground">Innovation:</span> Using AI to extract insights from complex data</li>
                </ul>
              </section>

              {/* Technology Approach */}
              <section>
                <h2 className="text-2xl font-bold mb-3 text-primary">Our Technology</h2>
                <ul className="space-y-2 text-muted-foreground">
                  <li><span className="font-semibold text-foreground">AI-Powered Search:</span> Vector embeddings and semantic search for natural language queries</li>
                  <li><span className="font-semibold text-foreground">Automated Data Collection:</span> Regular scraping of defense contract data</li>
                  <li><span className="font-semibold text-foreground">User-Friendly Interface:</span> Clean design that works on all devices</li>
                </ul>
              </section>

              {/* Future Vision */}
              <section>
                <h2 className="text-2xl font-bold mb-3 text-primary">Our Vision</h2>
                <p className="text-muted-foreground">
                  We&apos;re expanding beyond DoD contracts to all government spending, creating a comprehensive platform 
                  that connects disparate data sources and enables citizens to engage more deeply with how their tax dollars are spent.
                </p>
              </section>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-muted py-6">
        <div className="mx-auto w-full max-w-[800px] px-4 sm:px-6 lg:px-8 text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} GovWatch. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
} 