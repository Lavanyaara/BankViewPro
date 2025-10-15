import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, Institution, InstitutionDetail, CategoryScores, ChatMessage } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  institutions = signal<Institution[]>([]);
  selectedInstitution = signal<string>('');
  institutionDetail = signal<InstitutionDetail | null>(null);
  scores = signal<CategoryScores | null>(null);
  activeTab = signal<string>('overview');
  commentary = signal<Record<string, string>>({});
  loading = signal<boolean>(false);

  // Chat state
  chatMessages = signal<ChatMessage[]>([]);
  chatInput = '';
  chatLoading = signal<boolean>(false);

  // Flow toggle state
  useAlternateFlow = signal<boolean>(false);

  // Regular property for ngModel binding
  selectedInstitutionName = '';
  useAlternateFlowValue = false;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadInstitutions();
  }

  loadInstitutions() {
    this.apiService.getInstitutions().subscribe({
      next: (data) => {
        this.institutions.set(data);
        if (data.length > 0) {
          this.selectedInstitutionName = data[0].name;
          this.selectInstitution(data[0].name);
        }
      },
      error: (err) => console.error('Error loading institutions:', err)
    });
  }

  onInstitutionChange() {
    this.selectInstitution(this.selectedInstitutionName);
  }

  onToggleFlowChange() {
    this.useAlternateFlow.set(this.useAlternateFlowValue);
    if (this.selectedInstitutionName) {
      this.selectInstitution(this.selectedInstitutionName);
    }
  }

  selectInstitution(name: string) {
    this.selectedInstitution.set(name);
    this.selectedInstitutionName = name;
    this.loading.set(true);
    this.chatMessages.set([]); // Clear chat history when institution changes
    
    this.apiService.getInstitutionDetail(name, this.useAlternateFlow()).subscribe({
      next: (data) => {
        this.institutionDetail.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error loading institution detail:', err);
        this.loading.set(false);
      }
    });

    this.apiService.getInstitutionScores(name, this.useAlternateFlow()).subscribe({
      next: (data) => this.scores.set(data),
      error: (err) => console.error('Error loading scores:', err)
    });

    ['overview', 'capitalization', 'asset_quality', 'profitability', 'liquidity'].forEach(category => {
      this.loadCommentary(name, category);
    });
  }

  loadCommentary(institutionName: string, category: string) {
    this.apiService.getCommentary(institutionName, category, this.useAlternateFlow()).subscribe({
      next: (data) => {
        const current = this.commentary();
        this.commentary.set({ ...current, [category]: data.commentary });
      },
      error: (err) => console.error(`Error loading ${category} commentary:`, err)
    });
  }

  setActiveTab(tab: string) {
    this.activeTab.set(tab);
  }

  getLatestData() {
    const detail = this.institutionDetail();
    if (!detail || !detail.historical_data.length) return null;
    return detail.historical_data[detail.historical_data.length - 1];
  }

  getPreviousData() {
    const detail = this.institutionDetail();
    if (!detail || detail.historical_data.length < 2) return null;
    return detail.historical_data[detail.historical_data.length - 2];
  }

  calculateChange(current: number, previous: number): string {
    if (!previous) return '0.0';
    const change = ((current - previous) / previous) * 100;
    return change > 0 ? `+${change.toFixed(1)}` : change.toFixed(1);
  }

  getRatingColor(score: number): string {
    if (score >= 8.5) return '#2E7D32'; // Dark green
    if (score >= 7.0) return '#558B2F'; // Green
    if (score >= 5.5) return '#F9A825'; // Yellow
    if (score >= 4.0) return '#FF8F00'; // Orange
    return '#C62828'; // Red
  }

  sendChatMessage() {
    if (!this.chatInput.trim() || !this.selectedInstitution()) {
      return;
    }

    const messageToSend = this.chatInput;
    const currentHistory = [...this.chatMessages()];
    
    const userMessage: ChatMessage = {
      role: 'user',
      content: messageToSend,
      timestamp: new Date()
    };

    this.chatMessages.set([...currentHistory, userMessage]);
    this.chatInput = '';
    this.chatLoading.set(true);

    this.apiService.sendChatMessage({
      institutionName: this.selectedInstitution(),
      message: messageToSend,
      conversationHistory: currentHistory,
      useAlternateFlow: this.useAlternateFlow()
    }).subscribe({
      next: (response) => {
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.message,
          timestamp: new Date()
        };
        this.chatMessages.set([...currentHistory, userMessage, assistantMessage]);
        this.chatLoading.set(false);
      },
      error: (err) => {
        console.error('Error sending chat message:', err);
        this.chatLoading.set(false);
      }
    });
  }
}
