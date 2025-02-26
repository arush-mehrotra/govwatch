"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Loader2, ExternalLink, Calendar, DollarSign, Building2, FileText, Tag } from "lucide-react"
import { Badge } from "@/components/ui/badge"

interface SearchResultsProps {
  stream: ReadableStream<Uint8Array> | null
  isLoading: boolean
  error: string | null
}

interface Source {
  url: string;
  date: string;
  section: string;
}

interface ParsedResult {
  answer: string;
  sources: Source[];
}

export function SearchResults({ stream, isLoading, error }: SearchResultsProps) {
  const [streamedText, setStreamedText] = useState<string>("")
  const [isProcessing, setIsProcessing] = useState<boolean>(false)
  const [parsedResult, setParsedResult] = useState<ParsedResult | null>(null)
  const [streamError, setStreamError] = useState<string | null>(null)

  useEffect(() => {
    if (!stream) return

    setIsProcessing(true)
    setStreamedText("")
    setParsedResult(null)
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
            // Parse the text as it comes in
            parseStreamedText(newText)
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

  // Function to parse the streamed text into structured data
  const parseStreamedText = (text: string) => {
    // Check if the text contains sources section
    const sourcesSplit = text.split('--- Sources ---');
    
    if (sourcesSplit.length > 1) {
      const answer = sourcesSplit[0].trim();
      const sourcesText = sourcesSplit[1].trim();
      
      // Parse sources
      const sourceLines = sourcesText.split('\n').filter(line => line.trim() !== '');
      const sources: Source[] = [];
      
      sourceLines.forEach(line => {
        // Extract URL, date, and section from source line
        // Format: "1. https://www.defense.gov/News/Contracts/Contract/Article/4069639/ (2025-02-18) - NAVY"
        const urlMatch = line.match(/https?:\/\/[^\s)]+/);
        const dateMatch = line.match(/\(([^)]+)\)/);
        const sectionMatch = line.match(/- ([^)]+)$/);
        
        if (urlMatch) {
          sources.push({
            url: urlMatch[0],
            date: dateMatch ? dateMatch[1].trim() : '',
            section: sectionMatch ? sectionMatch[1].trim() : ''
          });
        }
      });
      
      setParsedResult({ answer, sources });
    }
  }

  // Function to format contract amounts with highlighting
  const formatContractAmount = (text: string) => {
    return text.replace(
      /\$[\d,]+(\.\d+)?[MBK]?/g,
      match => (
        <span className="text-green-500 font-bold">{match}</span>
      )
    );
  }

  // Render the answer with formatting
  const renderAnswer = (answer: string) => {
    // Split by paragraphs
    const paragraphs = answer.split('\n\n').filter(p => p.trim() !== '');
    
    return (
      <div className="space-y-5">
        {paragraphs.map((paragraph, idx) => {
          // Check if it's a bullet point list
          if (paragraph.includes('* ')) {
            const items = paragraph.split('* ').filter(item => item.trim() !== '');
            return (
              <ul key={idx} className="space-y-4 list-none">
                {items.map((item, itemIdx) => (
                  <li key={itemIdx} className="pl-4 border-l-2 border-primary/20 py-2 hover:border-primary/50 transition-colors">
                    <div dangerouslySetInnerHTML={{ 
                      __html: item
                        .replace(/\*\*([^*]+)\*\*/g, '<span class="font-semibold text-primary">$1</span>')
                        .replace(/\$[\d,]+(\.\d+)?[MBK]?/g, '<span class="text-emerald-500 font-medium">$&</span>')
                        .replace(/\b\d{4}-\d{2}-\d{2}\b/g, '<span class="text-blue-400">$&</span>')
                        .replace(/"text-green-400 font-bold">/g, '"text-emerald-500 font-medium">')
                        .replace(/"text-blue-400">/g, '"text-blue-400">')
                    }} />
                  </li>
                ))}
              </ul>
            );
          } else {
            // Regular paragraph
            return (
              <p key={idx} className="leading-relaxed text-foreground/90" dangerouslySetInnerHTML={{ 
                __html: paragraph
                  .replace(/\*\*([^*]+)\*\*/g, '<span class="font-semibold text-primary">$1</span>')
                  .replace(/\$[\d,]+(\.\d+)?[MBK]?/g, '<span class="text-emerald-500 font-medium">$&</span>')
                  .replace(/\b\d{4}-\d{2}-\d{2}\b/g, '<span class="text-blue-400">$&</span>')
                  .replace(/"text-green-400 font-bold">/g, '"text-emerald-500 font-medium">')
                  .replace(/"text-blue-400">/g, '"text-blue-400">')
              }} />
            );
          }
        })}
      </div>
    );
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
      <div className="mt-6 space-y-5">
        <Card className="bg-secondary/40 border-muted rounded-2xl shadow-md overflow-hidden">
          <CardHeader className="pb-2 flex flex-row items-center justify-between bg-secondary/60 border-b border-muted/20">
            <CardTitle className="text-primary flex items-center gap-2">
              <FileText className="h-4 w-4" />
              {isProcessing ? "Processing Results..." : "Search Results"}
            </CardTitle>
            {isProcessing && (
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
            )}
          </CardHeader>
          <CardContent className="pt-5">
            {parsedResult ? (
              renderAnswer(parsedResult.answer)
            ) : (
              <div className="whitespace-pre-wrap">{streamedText}</div>
            )}
          </CardContent>
        </Card>
        
        {parsedResult && parsedResult.sources.length > 0 && (
          <Card className="bg-secondary/40 border-muted rounded-2xl shadow-md overflow-hidden">
            <CardHeader className="pb-2 bg-secondary/60 border-b border-muted/20">
              <CardTitle className="text-primary text-sm flex items-center gap-2">
                <ExternalLink className="h-4 w-4" />
                Sources
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {parsedResult.sources.map((source, idx) => (
                  <a 
                    key={idx} 
                    href={source.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex flex-col p-3 rounded-lg bg-background/50 hover:bg-background transition-colors border border-muted/50 hover:border-primary/20 hover:shadow-sm"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-medium bg-primary/5 text-primary/80 px-2 py-0.5 rounded">
                        {idx + 1}
                      </span>
                      {source.section && (
                        <Badge variant="outline" className="text-xs text-muted-foreground">
                          <Tag className="h-3 w-3 mr-1 opacity-70" />
                          {source.section}
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Calendar className="h-3 w-3 opacity-70" />
                      <span>{source.date || "No date"}</span>
                    </div>
                    <div className="mt-1 text-xs text-primary/70 truncate hover:text-primary">
                      {source.url.replace(/^https?:\/\//, '')}
                    </div>
                  </a>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    )
  }

  return null
} 