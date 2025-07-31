import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'
import ClientAuthProvider from '@/components/providers/ClientAuthProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment',
  description: 'Advanced digital system for intelligent document analysis, test generation, and AI-assisted learning.',
  keywords: ['education', 'AI', 'RAG', 'test generation', 'document analysis', 'learning'],
  authors: [{ name: 'DISCERA Team' }],
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        <ClientAuthProvider>
          {children}
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'hsl(var(--background))',
                color: 'hsl(var(--foreground))',
                border: '1px solid hsl(var(--border))',
              },
            }}
          />
        </ClientAuthProvider>
      </body>
    </html>
  )
} 