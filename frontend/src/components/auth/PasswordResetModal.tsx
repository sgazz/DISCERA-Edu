'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/modal'
import { authAPI } from '@/lib/api/client'
import toast from 'react-hot-toast'
import { Mail, ArrowLeft, Send } from 'lucide-react'
import { motion } from 'framer-motion'

interface PasswordResetModalProps {
  trigger?: React.ReactNode
}

export default function PasswordResetModal({ trigger }: PasswordResetModalProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // TODO: Implement actual password reset API call
      // await authAPI.resetPassword(email)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setSent(true)
      toast.success('Link za resetovanje lozinke je poslat na vaš email!')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Greška pri slanju email-a'
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setIsOpen(false)
    setEmail('')
    setSent(false)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        {trigger || (
          <Button variant="link" className="text-sm text-blue-600 hover:text-blue-800 p-0 h-auto">
            Zaboravili ste lozinku?
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-center">
            Resetovanje lozinke
          </DialogTitle>
        </DialogHeader>

        {!sent ? (
          <motion.form
            onSubmit={handleSubmit}
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <motion.p 
              className="text-sm text-gray-600 text-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
            >
              Unesite vašu email adresu i poslaćemo vam link za resetovanje lozinke.
            </motion.p>

            <motion.div 
              className="space-y-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Label htmlFor="reset-email">Email adresa</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="reset-email"
                  type="email"
                  placeholder="vas@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                />
              </div>
            </motion.div>

            <motion.div
              className="flex gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Button
                type="button"
                variant="outline"
                onClick={handleClose}
                className="flex-1"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Nazad
              </Button>
              <Button
                type="submit"
                className="flex-1"
                disabled={loading}
              >
                {loading ? (
                  'Slanje...'
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Pošalji
                  </>
                )}
              </Button>
            </motion.div>
          </motion.form>
        ) : (
          <motion.div
            className="text-center space-y-4"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
            >
              <Mail className="h-8 w-8 text-green-600" />
            </motion.div>
            
            <motion.h3 
              className="text-lg font-semibold"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              Email poslat!
            </motion.h3>
            
            <motion.p 
              className="text-sm text-gray-600"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              Proverite vašu email adresu i pratite instrukcije za resetovanje lozinke.
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Button onClick={handleClose} className="w-full">
                Zatvori
              </Button>
            </motion.div>
          </motion.div>
        )}
      </DialogContent>
    </Dialog>
  )
} 