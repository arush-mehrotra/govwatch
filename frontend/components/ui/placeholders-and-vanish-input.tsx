"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { ButtonSearch } from "@/components/ui/button-search"

export const PlaceholdersAndVanishInput = ({
  placeholders,
  onChange,
  onSubmit,
}: {
  placeholders: string[]
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void
}) => {
  const [currentPlaceholder, setCurrentPlaceholder] = useState("")
  const [currentPlaceholderIndex, setCurrentPlaceholderIndex] = useState(0)
  const [currentCharIndex, setCurrentCharIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const typingInterval = 50 // Typing speed
    const deletingInterval = 30 // Deleting speed
    const pauseDuration = 1500 // Pause before deleting

    const type = () => {
      const currentText = placeholders[currentPlaceholderIndex]

      if (!isDeleting) {
        // Typing
        if (currentCharIndex < currentText.length) {
          setCurrentPlaceholder(currentText.substring(0, currentCharIndex + 1))
          setCurrentCharIndex((prev) => prev + 1)
        } else {
          // Pause before deleting
          setTimeout(() => setIsDeleting(true), pauseDuration)
          return
        }
      } else {
        // Deleting
        if (currentCharIndex > 0) {
          setCurrentPlaceholder(currentText.substring(0, currentCharIndex - 1))
          setCurrentCharIndex((prev) => prev - 1)
        } else {
          setIsDeleting(false)
          setCurrentPlaceholderIndex((prev) => (prev + 1) % placeholders.length)
          return
        }
      }
    }

    const timer = setTimeout(type, isDeleting ? deletingInterval : typingInterval)
    return () => clearTimeout(timer)
  }, [currentCharIndex, currentPlaceholderIndex, isDeleting, placeholders])

  return (
    <form onSubmit={onSubmit} className="relative flex w-full max-w-2xl items-center justify-center mx-auto">
      <div className="flex w-full items-center gap-2">
        <input
          type="text"
          onChange={onChange}
          placeholder={currentPlaceholder}
          className="h-12 w-full rounded-full border border-muted bg-secondary/50 px-4 text-lg text-foreground placeholder:text-muted-foreground/70 focus:outline-none focus:ring-2 focus:ring-primary/20"
          autoComplete="off"
        />
        <ButtonSearch />
      </div>
    </form>
  )
}

