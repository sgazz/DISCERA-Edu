'use client'

import React, { useState, useEffect, createContext, useContext } from 'react'
import { User, AuthResponse } from '@/types'
import { authAPI } from '@/lib/api/client'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (userData: any) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const login = async (email: string, password: string) => {
    try {
      const response: AuthResponse = await authAPI.login(email, password)
      localStorage.setItem('discera_token', response.access_token)
      setUser(response.user)
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async (userData: any) => {
    try {
      console.log('useAuth register called with:', userData)
      const response = await authAPI.register(userData)
      console.log('useAuth register response:', response)
      // After registration, automatically log in
      await login(userData.email, userData.password)
    } catch (error) {
      console.error('useAuth register error:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('discera_token')
    setUser(null)
  }

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('discera_token')
      if (token) {
        const userData = await authAPI.me()
        setUser(userData)
      }
    } catch (error) {
      console.error('Auth check error:', error)
      localStorage.removeItem('discera_token')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    checkAuth()
  }, [])

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    checkAuth,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
} 