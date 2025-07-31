'use client'

import { useLocale, useTranslations } from 'next-intl'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Globe } from 'lucide-react'
import { motion } from 'framer-motion'

export default function LanguageSwitcher() {
  const locale = useLocale()
  const router = useRouter()
  const pathname = usePathname()
  const t = useTranslations()

  const switchLanguage = (newLocale: string) => {
    // Remove the current locale from the pathname
    const pathWithoutLocale = pathname.replace(`/${locale}`, '')
    
    // Navigate to the new locale
    router.push(`/${newLocale}${pathWithoutLocale}`)
  }

  return (
    <motion.div
      className="flex items-center space-x-2"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <Globe className="h-4 w-4 text-gray-500" />
      <div className="flex rounded-md border border-gray-200 bg-white">
        <motion.button
          onClick={() => switchLanguage('en')}
          className={`px-3 py-1 text-sm font-medium transition-colors ${
            locale === 'en'
              ? 'bg-blue-600 text-white'
              : 'text-gray-600 hover:text-gray-900'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          EN
        </motion.button>
        <motion.button
          onClick={() => switchLanguage('sr')}
          className={`px-3 py-1 text-sm font-medium transition-colors ${
            locale === 'sr'
              ? 'bg-blue-600 text-white'
              : 'text-gray-600 hover:text-gray-900'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          SR
        </motion.button>
      </div>
    </motion.div>
  )
} 