import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface ResearchResponse {
    answer: string;
    confidence_score: number;
    source_chunk_ids: string[];
}

export const api = {
    ingest: async (source: string) => {
        const response = await axios.post(`${API_URL}/ingest`, { source });
        return response.data;
    },
    ingestText: async (text: string) => {
        const response = await axios.post(`${API_URL}/ingest/text`, { text });
        return response.data;
    },
    ingestFile: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(`${API_URL}/ingest/file`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },
    research: async (query: string) => {
        const response = await axios.post<ResearchResponse>(`${API_URL}/research`, { query });
        return response.data;
    }
};
