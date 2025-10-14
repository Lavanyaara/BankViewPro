import { Institution } from '../../../shared/interfaces';

interface CacheEntry {
  data: Institution;
  timestamp: number;
  analysisText: string;
}

export class EdgarCache {
  private static cache: Map<string, CacheEntry> = new Map();
  private static readonly CACHE_TTL = 24 * 60 * 60 * 1000; // 24 hours

  static set(institutionName: string, data: Institution, analysisText: string): void {
    this.cache.set(institutionName, {
      data,
      timestamp: Date.now(),
      analysisText
    });
  }

  static get(institutionName: string): { data: Institution; analysisText: string } | null {
    const entry = this.cache.get(institutionName);
    
    if (!entry) {
      return null;
    }

    // Check if cache is still valid
    if (Date.now() - entry.timestamp > this.CACHE_TTL) {
      this.cache.delete(institutionName);
      return null;
    }

    return {
      data: entry.data,
      analysisText: entry.analysisText
    };
  }

  static clear(institutionName?: string): void {
    if (institutionName) {
      this.cache.delete(institutionName);
    } else {
      this.cache.clear();
    }
  }

  static has(institutionName: string): boolean {
    const entry = this.cache.get(institutionName);
    if (!entry) return false;
    
    // Check if still valid
    if (Date.now() - entry.timestamp > this.CACHE_TTL) {
      this.cache.delete(institutionName);
      return false;
    }
    
    return true;
  }
}
