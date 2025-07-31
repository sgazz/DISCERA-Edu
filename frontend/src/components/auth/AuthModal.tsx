'use client'

import { useState } from 'react'
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
import PasswordResetModal from './PasswordResetModal'
import SocialLogin from './SocialLogin'

export default function AuthModal() {
  const [isOpen, setIsOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [showSocialLogin, setShowSocialLogin] = useState(true)
  
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

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await login(loginData.email, loginData.password)
      
      // Save remember me preference
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
    
    if (registerData.password !== registerData.confirmPassword) {
      toast.error('Lozinke se ne poklapaju')
      return
    }

    if (registerData.password.length < 6) {
      toast.error('Lozinka mora imati najmanje 6 karaktera')
      return
    }

    setLoading(true)

    try {
      const { confirmPassword, ...registerPayload } = registerData
      await register(registerPayload)
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
      const message = error.response?.data?.detail || 'Greška pri registraciji'
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

  // Load remembered email on modal open
  const handleModalOpen = (open: boolean) => {
    setIsOpen(open)
    if (open && activeTab === 'login') {
      const rememberedEmail = localStorage.getItem('discera_remember_email')
      const rememberMe = localStorage.getItem('discera_remember_me')
      
      if (rememberedEmail && rememberMe === 'true') {
        setLoginData(prev => ({ ...prev, email: rememberedEmail }))
        setRememberMe(true)
      }
    }
  }

  const handleSocialLogin = (provider: string) => {
    toast(`${provider} login će biti implementiran uskoro!`, {
      icon: '🔧',
      style: {
        borderRadius: '10px',
        background: '#333',
        color: '#fff',
      },
    })
  }

  const handleEmailLogin = () => {
    setShowSocialLogin(false)
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
            Login
          </Button>
        </motion.div>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-center">
            {activeTab === 'login' ? 'Prijavite se' : 'Registrujte se'}
          </DialogTitle>
        </DialogHeader>

        {/* Tab Navigation */}
        <motion.div 
          className="flex space-x-1 bg-muted p-1 rounded-lg mb-6"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <motion.button
            onClick={() => setActiveTab('login')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'login'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Prijava
          </motion.button>
          <motion.button
            onClick={() => setActiveTab('register')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'register'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Registracija
          </motion.button>
        </motion.div>

        {/* Form Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'login' && (
            <motion.div
              key="login"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              {showSocialLogin ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <SocialLogin
                    onGoogleLogin={() => handleSocialLogin('Google')}
                    onGithubLogin={() => handleSocialLogin('GitHub')}
                    onEmailLogin={handleEmailLogin}
                  />
                </motion.div>
              ) : (
                <motion.form
                  onSubmit={handleLogin}
                  className="space-y-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
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
                        placeholder="Unesite lozinku"
                        value={loginData.password}
                        onChange={handleLoginChange}
                        className="pl-10 pr-10"
                        required
                      />
                      <motion.button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </motion.button>
                    </div>
                  </motion.div>

                  <motion.div 
                    className="flex items-center justify-between"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.25 }}
                  >
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="remember-me"
                        checked={rememberMe}
                        onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                      />
                      <Label
                        htmlFor="remember-me"
                        className="text-sm font-normal cursor-pointer"
                      >
                        Zapamti me
                      </Label>
                    </div>
                    
                    <PasswordResetModal />
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
                      onClick={() => setShowSocialLogin(true)}
                      className="flex-1"
                    >
                      Nazad
                    </Button>
                    <Button
                      type="submit"
                      className="flex-1"
                      disabled={loading}
                    >
                      {loading ? 'Prijavljivanje...' : 'Prijavite se'}
                    </Button>
                  </motion.div>
                </motion.form>
              )}
            </motion.div>
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
                <Label htmlFor="register-full-name">Puno ime</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="register-full-name"
                    name="full_name"
                    type="text"
                    placeholder="Ime i prezime"
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
                    placeholder="Najmanje 6 karaktera"
                    value={registerData.password}
                    onChange={handleRegisterChange}
                    className="pl-10 pr-10"
                    required
                  />
                  <motion.button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </motion.button>
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
                    placeholder="Ponovite lozinku"
                    value={registerData.confirmPassword}
                    onChange={handleRegisterChange}
                    className="pl-10 pr-10"
                    required
                  />
                  <motion.button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </motion.button>
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
                  {loading ? 'Registracija...' : 'Registrujte se'}
                </Button>
              </motion.div>
            </motion.form>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  )
} 