'use client'

import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'
import { Chrome, Github, Mail } from 'lucide-react'

interface SocialLoginProps {
  onGoogleLogin?: () => void
  onGithubLogin?: () => void
  onEmailLogin?: () => void
}

export default function SocialLogin({ 
  onGoogleLogin, 
  onGithubLogin, 
  onEmailLogin 
}: SocialLoginProps) {
  const handleGoogleLogin = () => {
    // TODO: Implement Google OAuth
    console.log('Google login clicked')
    onGoogleLogin?.()
  }

  const handleGithubLogin = () => {
    // TODO: Implement GitHub OAuth
    console.log('GitHub login clicked')
    onGithubLogin?.()
  }

  const handleEmailLogin = () => {
    onEmailLogin?.()
  }

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Ili se prijavite sa
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3">
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Button
            variant="outline"
            onClick={handleGoogleLogin}
            className="w-full"
          >
            <Chrome className="mr-2 h-4 w-4" />
            Google
          </Button>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Button
            variant="outline"
            onClick={handleGithubLogin}
            className="w-full"
          >
            <Github className="mr-2 h-4 w-4" />
            GitHub
          </Button>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Button
            variant="outline"
            onClick={handleEmailLogin}
            className="w-full"
          >
            <Mail className="mr-2 h-4 w-4" />
            Email
          </Button>
        </motion.div>
      </div>
    </div>
  )
} 