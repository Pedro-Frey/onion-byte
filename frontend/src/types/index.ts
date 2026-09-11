export interface User {
  id: string;
  email: string;
  company_name: string;
}

export interface ScoreData {
  score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  breakdown: {
    company_fit: number;
    financial_health: number;
    online_presence: number;
  };
  recommendation: string;
}

export interface EnrichedData {
  social_profiles?: string[];
  company_info?: {
    size?: string;
    industry?: string;
    location?: string;
    revenue?: string;
  };
  online_presence?: {
    website?: string;
    domain_authority?: number;
  };
}

export interface Lead {
  id: string;
  nome: string;
  email: string;
  empresa: string;
  telefone?: string;
  cpf?: string;
  linkedin_url?: string;
  score_data?: ScoreData;
  enriched_data?: EnrichedData;
  status: 'NOVO' | 'EM_ENRIQUECIMENTO' | 'ENRIQUECIDO' | 'ERRO';
  created_at: string;
}

export interface ICP {
  id?: string;
  industries: string[];
  company_sizes: string[];
  job_titles: string[];
  locations: string[];
  revenue_range: string;
  custom_criteria: string[];
  deal_breakers: string[];
}

export interface UsageSummary {
  plan: string;
  requests_used: number;
  requests_limit: number;
  history: { date: string; count: number }[];
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
