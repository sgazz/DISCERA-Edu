import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import '../globals.css'
import { Toaster } from 'react-hot-toast'
import ClientAuthProvider from '@/components/providers/ClientAuthProvider'
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'

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

export default async function RootLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  const messages = await getMessages()

  return (
    <html lang={locale} className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        <NextIntlClientProvider messages={messages}>
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
        </NextIntlClientProvider>
      </body>
    </html>
  )
} 