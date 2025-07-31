'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/modal'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useAuth } from '@/hooks/useAuth'
import type { LoginForm, RegisterForm } from '@/types'
import toast from 'react-hot-toast'
import { Eye, EyeOff, Mail, Lock, User, UserPlus, LogIn } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function AuthModal() {
  const [isOpen, setIsOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  
  const { login, register } = useAuth()

  const [loginData, setLoginData] = useState<LoginForm>({
    email: '',
    password: '',
  })

  const [registerData, setRegisterData] = useState<RegisterForm>({
    email: '',
    username: '',
    full_name: '',
    password: '',
    confirmPassword: '',
    role: 'student',
  })

  // Load remembered email on component mount
  useEffect(() => {
    const rememberedEmail = localStorage.getItem('discera_remember_email')
    if (rememberedEmail) {
      setLoginData(prev => ({ ...prev, email: rememberedEmail }))
      setRememberMe(true)
    }
  }, [])

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validatePassword = (password: string) => {
    return password.length >= 6
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateEmail(loginData.email)) {
      toast.error('Unesite validnu email adresu')
      return
    }

    if (!validatePassword(loginData.password)) {
      toast.error('Lozinka mora imati najmanje 6 karaktera')
      return
    }

    setLoading(true)

    try {
      await login(loginData.email, loginData.password)
      
      // Handle remember me functionality
      if (rememberMe) {
        localStorage.setItem('discera_remember_me', 'true')
        localStorage.setItem('discera_remember_email', loginData.email)
      } else {
        localStorage.removeItem('discera_remember_me')
        localStorage.removeItem('discera_remember_email')
      }
      
      toast.success('Uspešno ste se prijavili!')
      setIsOpen(false)
      setLoginData({ email: '', password: '' })
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Greška pri prijavi'
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateEmail(registerData.email)) {
      toast.error('Unesite validnu email adresu')
      return
    }

    if (!validatePassword(registerData.password)) {
      toast.error('Lozinka mora imati najmanje 6 karaktera')
      return
    }

    if (registerData.password !== registerData.confirmPassword) {
      toast.error('Lozinke se ne poklapaju')
      return
    }

    if (registerData.username.length < 3) {
      toast.error('Korisničko ime mora imati najmanje 3 karaktera')
      return
    }

    if (registerData.full_name.length < 2) {
      toast.error('Ime i prezime mora imati najmanje 2 karaktera')
      return
    }

    setLoading(true)

    try {
      const { confirmPassword, ...registerPayload } = registerData
      console.log('Sending registration data:', registerPayload)
      
      const response = await register(registerPayload)
      console.log('Registration response:', response)
      
      toast.success('Uspešno ste se registrovali!')
      setIsOpen(false)
      setRegisterData({
        email: '',
        username: '',
        full_name: '',
        password: '',
        confirmPassword: '',
        role: 'student',
      })
    } catch (error: any) {
      console.error('Registration error:', error)
      console.error('Error response:', error.response)
      
      let message = 'Greška pri registraciji'
      if (error.response?.data?.detail) {
        message = error.response.data.detail
      } else if (error.message) {
        message = error.message
      }
      
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleRegisterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRegisterData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleRoleChange = (value: string) => {
    setRegisterData(prev => ({
      ...prev,
      role: value as 'student' | 'teacher' | 'admin'
    }))
  }

  const handleModalOpen = (open: boolean) => {
    setIsOpen(open)
    if (!open) {
      setLoginData({ email: '', password: '' })
      setRegisterData({
        email: '',
        username: '',
        full_name: '',
        password: '',
        confirmPassword: '',
        role: 'student',
      })
      setShowPassword(false)
      setShowConfirmPassword(false)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleModalOpen}>
      <DialogTrigger asChild>
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Button variant="outline" className="flex items-center gap-2">
            <LogIn className="h-4 w-4" />
            Prijavi se
          </Button>
        </motion.div>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-center">
            Dobrodošli u DISCERA
          </DialogTitle>
        </DialogHeader>

        <div className="flex space-x-1 mb-6">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              variant={activeTab === 'login' ? 'default' : 'outline'}
              onClick={() => setActiveTab('login')}
              className="flex items-center gap-2"
            >
              <LogIn className="h-4 w-4" />
              Prijava
            </Button>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              variant={activeTab === 'register' ? 'default' : 'outline'}
              onClick={() => setActiveTab('register')}
              className="flex items-center gap-2"
            >
              <UserPlus className="h-4 w-4" />
              Registracija
            </Button>
          </motion.div>
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'login' && (
            <motion.form
              key="login"
              onSubmit={handleLogin}
              className="space-y-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                <Label htmlFor="login-email">Email adresa</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="login-email"
                    name="email"
                    type="email"
                    placeholder="vas@email.com"
                    value={loginData.email}
                    onChange={handleLoginChange}
                    className="pl-10"
                    required
                  />
                </div>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Label htmlFor="login-password">Lozinka</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="login-password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Vaša lozinka"
                    value={loginData.password}
                    onChange={handleLoginChange}
                    className="pl-10 pr-10"
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </motion.div>

              <motion.div
                className="flex items-center space-x-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Checkbox
                  id="remember-me"
                  checked={rememberMe}
                  onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                />
                <Label htmlFor="remember-me" className="text-sm font-normal cursor-pointer">
                  Zapamti me
                </Label>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <Button
                  type="submit"
                  className="w-full"
                  disabled={loading}
                >
                  {loading ? 'Prijavljivanje...' : 'Prijavi se'}
                </Button>
              </motion.div>
            </motion.form>
          )}

          {activeTab === 'register' && (
            <motion.form
              key="register"
              onSubmit={handleRegister}
              className="space-y-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                <Label htmlFor="register-email">Email adresa</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-email"
                    name="email"
                    type="email"
                    placeholder="vas@email.com"
                    value={registerData.email}
                    onChange={handleRegisterChange}
                    className="pl-10"
                    required
                  />
                </div>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Label htmlFor="register-username">Korisničko ime</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-username"
                    name="username"
                    type="text"
                    placeholder="korisnicko_ime"
                    value={registerData.username}
                    onChange={handleRegisterChange}
                    className="pl-10"
                    required
                  />
                </div>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Label htmlFor="register-full-name">Ime i prezime</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-full-name"
                    name="full_name"
                    type="text"
                    placeholder="Ime Prezime"
                    value={registerData.full_name}
                    onChange={handleRegisterChange}
                    className="pl-10"
                    required
                  />
                </div>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <Label htmlFor="register-role">Uloga</Label>
                <Select value={registerData.role} onValueChange={handleRoleChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Izaberite ulogu" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="student">Student</SelectItem>
                    <SelectItem value="teacher">Nastavnik</SelectItem>
                    <SelectItem value="admin">Administrator</SelectItem>
                  </SelectContent>
                </Select>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Label htmlFor="register-password">Lozinka</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Vaša lozinka"
                    value={registerData.password}
                    onChange={handleRegisterChange}
                    className="pl-10 pr-10"
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <Label htmlFor="register-confirm-password">Potvrdite lozinku</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-confirm-password"
                    name="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    placeholder="Potvrdite lozinku"
                    value={registerData.confirmPassword}
                    onChange={handleRegisterChange}
                    className="pl-10 pr-10"
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
              >
                <Button
                  type="submit"
                  className="w-full"
                  disabled={loading}
                >
                  {loading ? 'Registracija...' : 'Registruj se'}
                </Button>
              </motion.div>
            </motion.form>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  )
} 