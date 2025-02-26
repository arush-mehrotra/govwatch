"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { BarChart3, Building2, DollarSign, FileText, Shield } from "lucide-react"
import { useState } from "react"
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input"
import Link from "next/link"
import { ButtonAbout } from "@/components/ui/button-about"

export default function Home() {
  const [searchValue, setSearchValue] = useState("")

  // DoD contracts-related placeholders
  const contractPlaceholders = [
    "Show me contracts over $10M in California last year",
    "Which contractors received the most funding in 2023?",
    "Find missile defense systems contracts",
    "Search for Navy contracts awarded to small businesses",
    "Show me aircraft procurement contracts since 2020"
  ]

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value)
    console.log(e.target.value)
  }

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log("Searching for:", searchValue)
    // Implement actual search functionality here
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="border-b border-muted">
        <div className="flex h-16 items-center justify-between px-8">
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold glow text-primary">GovWatch</span>
          </div>
          <nav className="flex gap-6">
            <Link href="/about">
              <ButtonAbout />
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <section className="hero-pattern border-b border-muted py-20">
          <div className="px-8">
            <h1 className="heading-serif mb-2 text-center text-5xl font-normal text-primary">
              Search DoD Contract Spending
            </h1>
            <p className="mb-8 text-center text-lg text-muted-foreground">
              Ask questions in plain English about Department of Defense contracts and spending
            </p>
            <div className="mx-auto flex max-w-2xl gap-2">
              <div className="w-full">
                <PlaceholdersAndVanishInput
                  placeholders={contractPlaceholders}
                  onChange={handleSearchChange}
                  onSubmit={handleSearchSubmit}
                />
              </div>
            </div>
          </div>
        </section>

        <section className="py-12">
          <div className="px-8">
            <div className="mb-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <Card className="bg-secondary/50 border-muted rounded-2xl">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Contracts</CardTitle>
                  <FileText className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">142,384</div>
                  <p className="text-xs text-muted-foreground">+20.1% from last year</p>
                </CardContent>
              </Card>
              <Card className="bg-secondary/50 border-muted rounded-2xl">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                  <DollarSign className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">$245.6B</div>
                  <p className="text-xs text-muted-foreground">+12.3% from last year</p>
                </CardContent>
              </Card>
              <Card className="bg-secondary/50 border-muted rounded-2xl">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Contractors</CardTitle>
                  <Building2 className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">2,464</div>
                  <p className="text-xs text-muted-foreground">+4.75% from last year</p>
                </CardContent>
              </Card>
              <Card className="bg-secondary/50 border-muted rounded-2xl">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Average Contract</CardTitle>
                  <BarChart3 className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">$1.72M</div>
                  <p className="text-xs text-muted-foreground">-3.2% from last year</p>
                </CardContent>
              </Card>
            </div>

            <div className="rounded-2xl border border-muted bg-secondary/50 overflow-hidden">
              <div className="border-b border-muted px-8 py-3">
                <h2 className="font-semibold text-primary">Recent Large Contracts</h2>
              </div>
              <Table>
                <TableHeader>
                  <TableRow className="hover:bg-secondary/80">
                    <TableHead className="text-muted-foreground">Contractor</TableHead>
                    <TableHead className="text-muted-foreground">Description</TableHead>
                    <TableHead className="text-muted-foreground">Date</TableHead>
                    <TableHead className="text-right text-muted-foreground">Value</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow className="hover:bg-secondary/80">
                    <TableCell className="font-medium text-primary">Lockheed Martin Corp.</TableCell>
                    <TableCell>F-35 Lightning II Fighter Aircraft</TableCell>
                    <TableCell>2024-02-15</TableCell>
                    <TableCell className="text-right">$712M</TableCell>
                  </TableRow>
                  <TableRow className="hover:bg-secondary/80">
                    <TableCell className="font-medium text-primary">Boeing Defense</TableCell>
                    <TableCell>CH-47F Chinook Helicopters</TableCell>
                    <TableCell>2024-02-12</TableCell>
                    <TableCell className="text-right">$543M</TableCell>
                  </TableRow>
                  <TableRow className="hover:bg-secondary/80">
                    <TableCell className="font-medium text-primary">Raytheon Technologies</TableCell>
                    <TableCell>Missile Defense Systems</TableCell>
                    <TableCell>2024-02-10</TableCell>
                    <TableCell className="text-right">$489M</TableCell>
                  </TableRow>
                  <TableRow className="hover:bg-secondary/80">
                    <TableCell className="font-medium text-primary">General Dynamics</TableCell>
                    <TableCell>Combat Vehicle Upgrades</TableCell>
                    <TableCell>2024-02-08</TableCell>
                    <TableCell className="text-right">$367M</TableCell>
                  </TableRow>
                  <TableRow className="hover:bg-secondary/80">
                    <TableCell className="font-medium text-primary">Northrop Grumman</TableCell>
                    <TableCell>Surveillance Systems</TableCell>
                    <TableCell>2024-02-05</TableCell>
                    <TableCell className="text-right">$298M</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-muted py-6">
        <div className="px-8 text-center text-sm text-muted-foreground">
          GovWatch - Making Department of Defense spending transparent and accessible.
        </div>
      </footer>
    </div>
  )
}

