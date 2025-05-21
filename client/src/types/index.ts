export interface Campaign {
    id: number;
    campaign_name: string;
    platform: string;
    region: string;
    date: string;
    impressions: number;
    clicks: number;
    conversions: number;
    spend: number;
    ctr: number;
    cpc: number;
    cpa: number;
    created_at: string;
}

export interface Analysis {
    id: number;
    type: string;
    metric: string;
    description: string;
    severity: 'low' | 'medium' | 'high';
    value: number | null;
    expected_value: number | null;
    date_range_start: string | null;
    date_range_end: string | null;
    created_at: string;
    notified: boolean;
}

export interface Recommendation {
    id: number;
    analysis_id: number;
    content: string;
    created_at: string;
}

export interface AnalysisWithRecommendations extends Analysis {
    recommendations: Recommendation[];
}