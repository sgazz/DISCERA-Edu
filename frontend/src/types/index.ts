export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: 'student' | 'teacher' | 'admin'
  is_active: boolean
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Document {
  id: number
  title: string
  filename: string
  file_size: number
  file_type: string
  is_processed: boolean
  created_at: string
}

export interface ChatMessage {
  id: string
  message: string
  response: string
  sources: string[]
  timestamp: Date
  documentId?: number
}

export interface DocumentAnalysis {
  key_concepts: string[]
  summary: string
  difficulty_level: string
  estimated_reading_time: string
  topics: string[]
}

export interface Test {
  id: number
  title: string
  description: string
  questions: Question[]
  created_at: string
  created_by: number
}

export interface Question {
  id: number
  question: string
  type: 'multiple_choice' | 'true_false' | 'short_answer'
  options?: string[]
  correct_answer?: string
  points: number
}

export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  email: string
  username: string
  full_name: string
  password: string
  confirmPassword: string
  role: 'student' | 'teacher' | 'admin'
}

export interface ApiError {
  detail: string
  status_code?: number
} 