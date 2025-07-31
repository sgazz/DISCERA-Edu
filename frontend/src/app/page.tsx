'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import AuthModal from '@/components/auth/AuthModal'
import {
  BookOpen,
  MessageSquare,
  Upload,
  Brain,
  FileText,
  Users,
  Zap,
  Shield,
  BarChart3
} from 'lucide-react'
import toast from 'react-hot-toast'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)

  const features = [
    {
      icon: <BookOpen className="h-6 w-6" />,
      title: "Document Management",
      description: "Upload and process PDF, DOCX, and TXT files with intelligent text extraction and semantic chunking."
    },
    {
      icon: <Brain className="h-6 w-6" />,
      title: "RAG System",
      description: "Advanced Retrieval Augmented Generation with ChromaDB vector storage and semantic search."
    },
    {
      icon: <MessageSquare className="h-6 w-6" />,
      title: "AI Chat",
      description: "Context-aware AI conversations powered by OpenAI GPT-4 with document understanding."
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: "Test Generation",
      description: "AI-powered automatic test creation with multiple question types and difficulty levels."
    },
    {
      icon: <BarChart3 className="h-6 w-6" />,
      title: "Analytics",
      description: "Comprehensive progress tracking and learning insights with detailed performance metrics."
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Security",
      description: "JWT authentication with role-based access control and secure document handling."
    }
  ]

  const handleUploadClick = () => {
    toast.info('Upload functionality coming soon!')
  }

  const handleChatClick = () => {
    toast.info('AI Chat functionality coming soon!')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-md">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-2xl font-bold gradient-text">DISCERA</h1>
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">Features</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">About</a>
              <AuthModal />
              <Button>Get Started</Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">DISCERA</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Digital Intelligent System for Comprehensive Exam Review & Assessment
          </p>
          <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
            Advanced digital system for intelligent document analysis, test generation, and AI-assisted learning.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              onClick={handleUploadClick}
              className="h-11 rounded-md text-lg px-8 py-4"
            >
              <Upload className="mr-2 h-5 w-5" />
              Upload Documents
            </Button>
            <Button 
              onClick={handleChatClick}
              variant="outline" 
              className="h-11 rounded-md text-lg px-8 py-4"
            >
              <MessageSquare className="mr-2 h-5 w-5" />
              Start Chat
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
          <p className="text-xl text-gray-600">Everything you need for intelligent education</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="card-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <CardTitle className="text-2xl">{feature.title}</CardTitle>
                <CardDescription className="text-sm">
                  {feature.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </section>

      {/* Try DISCERA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Try DISCERA</h2>
            <p className="text-xl text-gray-600">Experience the power of AI-assisted learning</p>
          </div>
          <Tabs defaultValue="chat" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="chat">AI Chat</TabsTrigger>
              <TabsTrigger value="upload">Upload</TabsTrigger>
              <TabsTrigger value="login">Login</TabsTrigger>
            </TabsList>
            <TabsContent value="chat" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>AI Assistant</CardTitle>
                  <CardDescription>Ask questions about your documents</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex space-x-2">
                    <Input placeholder="Ask a question..." />
                    <Button>Send</Button>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 min-h-[200px] flex items-center justify-center">
                    <p className="text-gray-500">Chat interface coming soon...</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="upload" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Document Upload</CardTitle>
                  <CardDescription>Upload your documents for analysis</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                    <p className="text-gray-500">Drag and drop your files here or click to browse</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="login" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Authentication</CardTitle>
                  <CardDescription>Login or create your account</CardDescription>
                </CardHeader>
                <CardContent className="text-center">
                  <AuthModal />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white border-t">
        <div className="container mx-auto px-4 py-20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">100%</div>
              <div className="text-gray-600">Backend Test Coverage</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">14</div>
              <div className="text-gray-600">API Endpoints</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">3</div>
              <div className="text-gray-600">File Formats Supported</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">DISCERA</h3>
              <p className="text-gray-400">Empowering education through intelligent document analysis and AI-assisted learning.</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Features</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Document Management</li>
                <li>AI Chat</li>
                <li>Test Generation</li>
                <li>Analytics</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Technology</h4>
              <ul className="space-y-2 text-gray-400">
                <li>FastAPI</li>
                <li>Next.js 14</li>
                <li>OpenAI GPT-4</li>
                <li>ChromaDB</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Documentation</li>
                <li>GitHub</li>
                <li>Issues</li>
                <li>Contact</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2025 DISCERA. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 