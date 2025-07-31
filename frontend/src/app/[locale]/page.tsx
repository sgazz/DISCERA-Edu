'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import AuthModal from '@/components/auth/AuthModal'
import LanguageSwitcher from '@/components/ui/language-switcher'
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
import { useTranslations } from 'next-intl'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)
  const t = useTranslations()

  const features = [
    {
      icon: <BookOpen className="h-6 w-6" />,
      title: t('features.documentManagement.title'),
      description: t('features.documentManagement.description')
    },
    {
      icon: <Brain className="h-6 w-6" />,
      title: t('features.ragSystem.title'),
      description: t('features.ragSystem.description')
    },
    {
      icon: <MessageSquare className="h-6 w-6" />,
      title: t('features.aiChat.title'),
      description: t('features.aiChat.description')
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: t('features.testGeneration.title'),
      description: t('features.testGeneration.description')
    },
    {
      icon: <BarChart3 className="h-6 w-6" />,
      title: t('features.analytics.title'),
      description: t('features.analytics.description')
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: t('features.security.title'),
      description: t('features.security.description')
    }
  ]

  const handleUploadClick = () => {
    toast(t('toast.uploadComingSoon'), {
      icon: '📁',
      style: {
        borderRadius: '10px',
        background: '#333',
        color: '#fff',
      },
    })
  }

  const handleChatClick = () => {
    toast(t('toast.chatComingSoon'), {
      icon: '🤖',
      style: {
        borderRadius: '10px',
        background: '#333',
        color: '#fff',
      },
    })
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
              <h1 className="text-2xl font-bold gradient-text">{t('app.name')}</h1>
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">{t('navigation.features')}</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">{t('navigation.about')}</a>
              <LanguageSwitcher />
              <AuthModal />
              <Button>{t('navigation.getStarted')}</Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">{t('hero.title')}</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            {t('hero.subtitle')}
          </p>
          <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
            {t('hero.description')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              onClick={handleUploadClick}
              className="h-11 rounded-md text-lg px-8 py-4"
            >
              <Upload className="mr-2 h-5 w-5" />
              {t('hero.uploadDocuments')}
            </Button>
            <Button 
              onClick={handleChatClick}
              variant="outline" 
              className="h-11 rounded-md text-lg px-8 py-4"
            >
              <MessageSquare className="mr-2 h-5 w-5" />
              {t('hero.startChat')}
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">{t('features.title')}</h2>
          <p className="text-xl text-gray-600">{t('features.subtitle')}</p>
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
            <h2 className="text-4xl font-bold mb-4">{t('trySection.title')}</h2>
            <p className="text-xl text-gray-600">{t('trySection.subtitle')}</p>
          </div>
          <Tabs defaultValue="chat" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="chat">{t('trySection.aiChat')}</TabsTrigger>
              <TabsTrigger value="upload">{t('trySection.upload')}</TabsTrigger>
              <TabsTrigger value="login">{t('trySection.login')}</TabsTrigger>
            </TabsList>
            <TabsContent value="chat" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>{t('trySection.aiAssistant')}</CardTitle>
                  <CardDescription>{t('trySection.askQuestions')}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex space-x-2">
                    <Input placeholder={t('trySection.askPlaceholder')} />
                    <Button>{t('trySection.send')}</Button>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 min-h-[200px] flex items-center justify-center">
                    <p className="text-gray-500">{t('trySection.chatComingSoon')}</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="upload" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>{t('trySection.documentUpload')}</CardTitle>
                  <CardDescription>{t('trySection.uploadDescription')}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                    <p className="text-gray-500">{t('trySection.dragDropText')}</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="login" className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>{t('trySection.authentication')}</CardTitle>
                  <CardDescription>{t('trySection.authDescription')}</CardDescription>
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
              <div className="text-gray-600">{t('stats.backendCoverage')}</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">14</div>
              <div className="text-gray-600">{t('stats.apiEndpoints')}</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">3</div>
              <div className="text-gray-600">{t('stats.fileFormats')}</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">{t('app.name')}</h3>
              <p className="text-gray-400">{t('footer.description')}</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">{t('footer.features')}</h4>
              <ul className="space-y-2 text-gray-400">
                <li>{t('features.documentManagement.title')}</li>
                <li>{t('features.aiChat.title')}</li>
                <li>{t('features.testGeneration.title')}</li>
                <li>{t('features.analytics.title')}</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">{t('footer.technology')}</h4>
              <ul className="space-y-2 text-gray-400">
                <li>FastAPI</li>
                <li>Next.js 14</li>
                <li>OpenAI GPT-4</li>
                <li>ChromaDB</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">{t('footer.support')}</h4>
              <ul className="space-y-2 text-gray-400">
                <li>{t('footer.documentation')}</li>
                <li>{t('footer.github')}</li>
                <li>{t('footer.issues')}</li>
                <li>{t('footer.contact')}</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>{t('footer.copyright')}</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 