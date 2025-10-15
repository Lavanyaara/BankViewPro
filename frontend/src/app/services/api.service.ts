import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Institution {
  name: string;
  type: string;
  assets: number;
  employees: number;
  branches: number;
}

export interface HistoricalRecord {
  year: number;
  capital_adequacy_ratio: number;
  tier1_ratio: number;
  leverage_ratio: number;
  risk_weighted_assets: number;
  npl_ratio: number;
  loan_loss_provisions: number;
  coverage_ratio: number;
  asset_classification: number;
  return_on_assets: number;
  return_on_equity: number;
  net_interest_margin: number;
  cost_to_income_ratio: number;
  earnings_per_share: number;
  liquidity_coverage_ratio: number;
  net_stable_funding_ratio: number;
  loan_to_deposit_ratio: number;
  cash_ratio: number;
}

export interface InstitutionDetail {
  institution_name: string;
  institution_type: string;
  assets: number;
  employees: number;
  branches: number;
  historical_data: HistoricalRecord[];
}

export interface CategoryScores {
  capitalization: number;
  asset_quality: number;
  profitability: number;
  liquidity: number;
  overall: number;
  rating: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  institutionName: string;
  message: string;
  conversationHistory: ChatMessage[];
  useAlternateFlow?: boolean;
}

export interface ChatResponse {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:3000/api';

  constructor(private http: HttpClient) {}

  getInstitutions(): Observable<Institution[]> {
    return this.http.get<Institution[]>(`${this.apiUrl}/institutions`);
  }

  getInstitutionDetail(name: string, useAlternateFlow: boolean = false): Observable<InstitutionDetail> {
    const params = useAlternateFlow ? '?overrideFlow=true' : '';
    return this.http.get<InstitutionDetail>(`${this.apiUrl}/institutions/${encodeURIComponent(name)}${params}`);
  }

  getInstitutionScores(name: string, useAlternateFlow: boolean = false): Observable<CategoryScores> {
    const params = useAlternateFlow ? '?overrideFlow=true' : '';
    return this.http.get<CategoryScores>(`${this.apiUrl}/institutions/${encodeURIComponent(name)}/scores${params}`);
  }

  getCommentary(institutionName: string, category: string, useAlternateFlow: boolean = false): Observable<{ commentary: string }> {
    return this.http.post<{ commentary: string }>(`${this.apiUrl}/commentary`, {
      institutionName,
      category,
      overrideFlow: useAlternateFlow
    });
  }

  getMetrics(): Observable<any> {
    return this.http.get(`${this.apiUrl}/metrics`);
  }

  sendChatMessage(request: ChatRequest): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, request);
  }
}
