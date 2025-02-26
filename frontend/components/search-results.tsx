"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Loader2 } from "lucide-react"

interface SearchResultsProps {
  stream: ReadableStream<Uint8Array> | null
  isLoading: boolean
  error: string | null
}

export function SearchResults({ stream, isLoading, error }: SearchResultsProps) {
  const [streamedText, setStreamedText] = useState<string>("")
  const [isProcessing, setIsProcessing] = useState<boolean>(false)
  const [formattedResults, setFormattedResults] = useState<JSX.Element | null>(null)
  const [streamError, setStreamError] = useState<string | null>(null)

  useEffect(() => {
    if (!stream) return

    setIsProcessing(true)
    setStreamedText("")
    setFormattedResults(null)
    setStreamError(null)

    const reader = stream.getReader()
    const decoder = new TextDecoder()

    async function readStream() {
      try {
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            setIsProcessing(false)
            break
          }
          
          const chunk = decoder.decode(value, { stream: true })
          setStreamedText(prev => {
            const newText = prev + chunk
            // Format the text as it comes in
            formatStreamedText(newText)
            return newText
          })
        }
      } catch (error) {
        console.error("Error reading stream:", error)
        setStreamError(`Error reading stream: ${error instanceof Error ? error.message : String(error)}`)
        setIsProcessing(false)
      }
    }

    readStream()

    return () => {
      reader.cancel().catch(console.error)
    }
  }, [stream])

  // Function to format the streamed text with highlighting
  const formatStreamedText = (text: string) => {
    // Split by newlines and format
    const lines = text.split('\n')
    
    const formattedJsx = (
      <div className="space-y-2">
        {lines.map((line, index) => {
          // Highlight dollar amounts
          const dollarHighlighted = line.replace(
            /\$[\d,]+(\.\d+)?[MBK]?/g, 
            match => `<span class="text-green-400 font-bold">${match}</span>`
          )
          
          // Highlight dates
          const dateHighlighted = dollarHighlighted.replace(
            /\b\d{4}-\d{2}-\d{2}\b/g,
            match => `<span class="text-blue-400">${match}</span>`
          )
          
          // Highlight contractor names (assuming they're in quotes or followed by Corp/Inc)
          const nameHighlighted = dateHighlighted.replace(
            /["']([^"']+)["']|(\w+\s+(Corp|Inc|LLC|Technologies|Systems|Dynamics|Martin|Defense))/g,
            match => `<span class="text-primary font-semibold">${match}</span>`
          )
          
          return (
            <p 
              key={index} 
              className="leading-relaxed"
              dangerouslySetInnerHTML={{ __html: nameHighlighted }}
            />
          )
        })}
      </div>
    )
    
    setFormattedResults(formattedJsx)
  }

  if (error || streamError) {
    return (
      <Card className="bg-secondary/50 border-muted rounded-2xl mt-6">
        <CardHeader className="pb-2 flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-red-500" />
          <CardTitle className="text-red-500">Error</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-400">{error || streamError}</p>
          <p className="text-muted-foreground mt-2 text-sm">
            Try refreshing the page or checking your network connection. 
            If the problem persists, the backend service might be unavailable.
          </p>
        </CardContent>
      </Card>
    )
  }

  if (isLoading && !isProcessing) {
    return (
      <Card className="bg-secondary/50 border-muted rounded-2xl mt-6">
        <CardHeader className="pb-2">
          <CardTitle className="text-primary">Searching...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center p-4">
            <div className="h-6 w-6 animate-spin rounded-full border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (isProcessing || streamedText) {
    return (
      <Card className="bg-secondary/50 border-muted rounded-2xl mt-6 shadow-lg">
        <CardHeader className="pb-2 flex flex-row items-center justify-between">
          <CardTitle className="text-primary">
            {isProcessing ? "Processing Results..." : "Search Results"}
          </CardTitle>
          {isProcessing && (
            <Loader2 className="h-4 w-4 animate-spin text-primary" />
          )}
        </CardHeader>
        <CardContent>
          {formattedResults || (
            <div className="whitespace-pre-wrap">{streamedText}</div>
          )}
        </CardContent>
      </Card>
    )
  }

  return null
} 