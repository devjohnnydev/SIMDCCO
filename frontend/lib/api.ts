/**
 * API Service - Axios client for backend communication
 */
import axios from 'axios'

// FORÇANDO CAMINHO RELATIVO - BUILD TIMESTAMP: 2026-03-24-1050
const SITE_API_PATH = '/api'

export const api = axios.create({
    baseURL: SITE_API_PATH,
    headers: {
        'Content-Type': 'application/json',
    },
})

console.log('SIMDCCO: API Base URL initialized:', SITE_API_PATH, 'at 2026-03-24-1050');

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// API endpoints
export const apiService = {
    // Auth
    login: (email: string, password: string) => {
        const formData = new URLSearchParams()
        formData.append('username', email)
        formData.append('password', password)
        return api.post('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    },

    getCurrentUser: () => api.get('/auth/me'),

    // Respondents
    validateRespondent: (data: {
        cpf: string
        email: string
        cnpj: string
        department_name?: string
    }) => api.post('/respondents/validate', data),

    registerConsent: (data: {
        cpf: string
        cnpj: string
        email: string
        consent_version?: string
    }) => api.post('/respondents/consent', data),

    // Questionnaires
    getAllQuestions: () => api.get('/questionnaires'),

    // Responses
    submitResponse: (data: {
        cpf: string
        cnpj: string
        department_id?: string
        answers: Record<string, number>
        session_id: string
        campaign_slug?: string
    }) => api.post('/responses/submit', data),

    // Organizations
    getOrganizations: () => api.get('/organizations'),
    getOrganization: (id: string) => api.get(`/organizations/${id}`),
    createOrganization: (data: {
        cnpj: string
        razao_social: string
        nome_fantasia?: string
    }) => api.post('/organizations', data),
    updateOrganization: (id: string, data: {
        razao_social?: string
        nome_fantasia?: string
    }) => api.put(`/organizations/${id}`, data),
    deleteOrganization: (id: string) => api.delete(`/organizations/${id}`),

    // Campaigns
    getCampaigns: () => api.get('/campaigns'),
    createCampaign: (data: {
        name: string
        description?: string
        start_date: string
        end_date?: string
        organization_id?: string
    }) => api.post('/campaigns', data),
    getCampaign: (id: string) => api.get(`/campaigns/${id}`),
    updateCampaign: (id: string, data: any) => api.patch(`/campaigns/${id}`, data),
    toggleCampaign: (id: string) => api.post(`/campaigns/${id}/toggle`),
    getCampaignAnalytics: (id: string) => api.get(`/campaigns/analytics/${id}`),
    getResponseDetail: (campaignId: string, responseId: string) =>
        api.get(`/campaigns/analytics/${campaignId}/responses/${responseId}`),

    // Analytics
    getOrganizationAnalytics: (departmentId?: string) =>
        api.get('/analytics/organization', { params: { department_id: departmentId } }),
    calculateAnalytics: (departmentId?: string) =>
        api.post('/analytics/calculate', null, { params: { department_id: departmentId } }),

    // Reports
    generateReport: (data: { report_type: string; department_id?: string }) =>
        api.post('/reports/generate', data),
    getReports: () => api.get('/reports'),
    downloadReport: (reportId: string) =>
        api.get(`/reports/${reportId}/download`, { responseType: 'blob' }),

    // Admin
    getAdminDashboard: () => api.get('/admin/dashboard'),

    // Demo
    submitDemo: (data: {
        nome: string
        email: string
        telefone: string
        empresa: string
        cargo?: string
        mensagem?: string
    }) => api.post('/demo/submit', data),

    getDemoLeads: () => api.get('/demo/leads'),
}

export default api
