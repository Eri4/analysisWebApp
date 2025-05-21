import axios from 'axios';
import type {Campaign, Analysis, AnalysisWithRecommendations} from '@/types';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getCampaigns = async () => {
    const response = await api.get<Campaign[]>('/campaigns');
    return response.data;
};

export const getAnalyses = async () => {
    const response = await api.get<Analysis[]>('/analyses');
    return response.data;
};

export const getAnalysisById = async (id: number) => {
    const response = await api.get<AnalysisWithRecommendations>(`/analyses/${id}`);
    return response.data;
};

export const runAnalysis = async () => {
    const response = await api.post('/analyses/run');
    return response.data;
};

export const generateRecommendation = async (analysisId: number) => {
    const response = await api.post(`/recommendations/generate/${analysisId}`);
    return response.data;
};

export default api;