import axios, { AxiosError } from 'axios';

// Use environment variable or default to localhost
const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000');

const api = axios.create({
    baseURL: `${API_URL}/api`,
    timeout: 60000, // 60 second timeout for long-running operations
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add response interceptor for better error handling
api.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        if (error.response) {
            // Server responded with error status
            const detail = (error.response.data as any)?.detail || error.message;
            throw new Error(detail);
        } else if (error.request) {
            // Request made but no response
            throw new Error('No response from server. Please check your connection.');
        } else {
            // Something else happened
            throw new Error(error.message || 'An unexpected error occurred');
        }
    }
);

// Helper to get config with headers
// Helper to get config with headers
const getConfig = (apiKey?: string) => {
    if (!apiKey) return {};
    return {
        headers: {
            'x-groq-api-key': apiKey
        }
    };
};

export const ingest = async (source: string) => {
    // Ingest is local, no API key needed
    const response = await api.post('/ingest', { source });
    return response.data;
};

export const ingestText = async (text: string) => {
    const response = await api.post('/ingest/text', { text });
    return response.data;
};

export const ingestFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    // No API key needed for file ingest
    const headers = {
        'Content-Type': 'multipart/form-data',
    };

    const response = await api.post('/ingest/file', formData, {
        headers,
        timeout: 120000, // 2 minutes for file upload
    });
    return response.data;
};

export const research = async (query: string, apiKey?: string) => {
    const response = await api.post('/research', { query }, getConfig(apiKey));
    return response.data;
};

export default { ingest, ingestText, ingestFile, research };
