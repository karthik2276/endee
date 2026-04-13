import axios from 'axios'

// Uses Vite proxy: /api -> http://localhost:8000
// Set VITE_API_URL in .env to override (e.g. for production)
const BASE = import.meta.env.VITE_API_URL || '/api'

export const api = axios.create({ baseURL: BASE, timeout: 90_000 })

// ── Types ──────────────────────────────────────────────────────────────────

export interface ComplaintResult {
  id: string
  text: string
  category: string
  similarity_score: number
  timestamp: string
}

export interface AddComplaintRequest {
  text: string
  category: string
  customer_id?: string
}

export interface AddComplaintResponse {
  id: string
  message: string
  category: string
  timestamp: string
}

export interface SearchRequest {
  query: string
  top_k?: number
  category_filter?: string
}

export interface SearchResponse {
  query: string
  results: ComplaintResult[]
  total_found: number
}

export interface AskRequest {
  question: string
  top_k?: number
}

export interface AskResponse {
  question: string
  answer: string
  retrieved_complaints: ComplaintResult[]
  model_used: string
}

export interface HealthResponse {
  status: string
  total_complaints: number
  embedding_model: string
  llm_model: string
}

// ── API calls ──────────────────────────────────────────────────────────────

export const addComplaint = (body: AddComplaintRequest) =>
  api.post<AddComplaintResponse>('/add-complaint', body).then(r => r.data)

export const searchComplaints = (body: SearchRequest) =>
  api.post<SearchResponse>('/search', body).then(r => r.data)

export const askQuestion = (body: AskRequest) =>
  api.post<AskResponse>('/ask', body).then(r => r.data)

export const getHealth = () =>
  api.get<HealthResponse>('/health').then(r => r.data)
