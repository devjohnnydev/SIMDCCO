"use client"

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, ArrowLeft, Loader2, AlertCircle, Users, BarChart3, TrendingUp, Eye } from 'lucide-react'
import { apiService } from '@/lib/api'

interface DepartmentStat {
    department_name: string
    response_count: number
    imco_average: number
    fdac_average: number
}

interface ResponseDetail {
    id: string
    department_name: string | null
    completed_at: string
    imco_overall: number
    fdac_overall: number
}

interface CampaignAnalytics {
    campaign_id: string
    campaign_name: string
    total_responses: number
    completion_rate: number
    imco_overall: number
    imco_vectors: Record<string, number>
    imco_dimensions: Record<string, number>
    fdac_overall: number
    fdac_dimensions: Record<string, number>
    department_stats: DepartmentStat[]
    recent_responses: ResponseDetail[]
}

interface IndividualResponse {
    id: string
    department_name: string | null
    completed_at: string
    started_at: string
    imco: {
        overall: number
        vectors: Record<string, number>
        dimensions: Record<string, number>
    }
    fdac: {
        overall: number
        dimensions: Record<string, number>
    }
    answers: Record<string, number>
}

export default function CampaignAnalyticsPage() {
    const params = useParams()
    const router = useRouter()
    const campaignId = params?.id as string

    const [analytics, setAnalytics] = useState<CampaignAnalytics | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedResponse, setSelectedResponse] = useState<IndividualResponse | null>(null)
    const [loadingResponse, setLoadingResponse] = useState(false)

    useEffect(() => {
        if (campaignId) {
            loadAnalytics()
        }
    }, [campaignId])

    const loadAnalytics = async () => {
        try {
            const response = await apiService.getCampaignAnalytics(campaignId)
            setAnalytics(response.data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao carregar analytics')
        } finally {
            setLoading(false)
        }
    }

    const loadResponseDetail = async (responseId: string) => {
        setLoadingResponse(true)
        try {
            const response = await apiService.getResponseDetail(campaignId, responseId)
            setSelectedResponse(response.data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao carregar resposta')
        } finally {
            setLoadingResponse(false)
        }
    }

    const getRiskColor = (score: number) => {
        if (score >= 4.0) return 'text-green-700 bg-green-100'
        if (score >= 3.0) return 'text-yellow-700 bg-yellow-100'
        if (score >= 2.0) return 'text-orange-700 bg-orange-100'
        return 'text-red-700 bg-red-100'
    }

    const getRiskLabel = (score: number) => {
        if (score >= 4.0) return 'Baixo Risco'
        if (score >= 3.0) return 'Risco Médio'
        if (score >= 2.0) return 'Risco Alto'
        return 'Risco Crítico'
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="h-12 w-12 animate-spin text-primary-900" />
            </div>
        )
    }

    if (!analytics) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <AlertCircle className="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                    <p className="text-neutral-600">Campanha não encontrada</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-neutral-50">
            {/* Header */}
            <nav className="bg-white border-b border-neutral-200 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <Link href="/admin/dashboard" className="flex items-center space-x-2">
                                <Shield className="h-6 w-6 text-primary-900" />
                                <span className="text-xl font-bold text-primary-900">SIMDCCO</span>
                            </Link>
                            <span className="text-neutral-400">/</span>
                            <h1 className="text-xl font-semibold text-neutral-900">{analytics.campaign_name}</h1>
                        </div>
                        <Link href="/admin/campaigns" className="btn-outline flex items-center">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Voltar
                        </Link>
                    </div>
                </div>
            </nav>

            <div className="container mx-auto px-6 py-8">
                {error && (
                    <div className="alert-danger mb-6 flex items-center">
                        <AlertCircle className="h-5 w-5 mr-2" />
                        {error}
                    </div>
                )}

                {/* Summary Cards */}
                <div className="grid md:grid-cols-4 gap-6 mb-8">
                    <div className="card">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-sm text-neutral-600">Total de Respostas</p>
                            <Users className="h-8 w-8 text-primary-900 opacity-20" />
                        </div>
                        <p className="text-3xl font-bold text-neutral-900">{analytics.total_responses}</p>
                    </div>

                    <div className="card">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-sm text-neutral-600">IMCO (Clima)</p>
                            <BarChart3 className="h-8 w-8 text-primary-900 opacity-20" />
                        </div>
                        <p className="text-3xl font-bold text-neutral-900">{analytics.imco_overall.toFixed(2)}</p>
                        <span className={`inline-block mt-2 px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(analytics.imco_overall)}`}>
                            {getRiskLabel(analytics.imco_overall)}
                        </span>
                    </div>

                    <div className="card">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-sm text-neutral-600">FDAC (Cultura)</p>
                            <TrendingUp className="h-8 w-8 text-secondary-700 opacity-20" />
                        </div>
                        <p className="text-3xl font-bold text-neutral-900">{analytics.fdac_overall.toFixed(2)}</p>
                        <span className={`inline-block mt-2 px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(analytics.fdac_overall)}`}>
                            {getRiskLabel(analytics.fdac_overall)}
                        </span>
                    </div>

                    <div className="card">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-sm text-neutral-600">Score Médio Geral</p>
                            <BarChart3 className="h-8 w-8 text-neutral-400 opacity-20" />
                        </div>
                        <p className="text-3xl font-bold text-neutral-900">
                            {((analytics.imco_overall + analytics.fdac_overall) / 2).toFixed(2)}
                        </p>
                    </div>
                </div>

                {/* IMCO Analysis */}
                <div className="card mb-8">
                    <h2 className="text-2xl font-bold text-neutral-900 mb-6">IMCO - Análise de Clima Organizacional</h2>

                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-neutral-700 mb-4">Vetores</h3>
                        <div className="space-y-3">
                            {Object.entries(analytics.imco_vectors).map(([vector, score]) => (
                                <div key={vector}>
                                    <div className="flex justify-between items-center mb-1">
                                        <span className="text-sm font-medium text-neutral-700">{vector}</span>
                                        <span className="text-sm font-bold text-neutral-900">{score.toFixed(2)}</span>
                                    </div>
                                    <div className="w-full bg-neutral-200 rounded-full h-2">
                                        <div
                                            className={`h-2 rounded-full ${score >= 4 ? 'bg-green-500' : score >= 3 ? 'bg-yellow-500' : 'bg-red-500'}`}
                                            style={{ width: `${(score / 5) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div>
                        <h3 className="text-lg font-semibold text-neutral-700 mb-4">Dimensões</h3>
                        <div className="grid md:grid-cols-2 gap-4">
                            {Object.entries(analytics.imco_dimensions).map(([dimension, score]) => (
                                <div key={dimension} className="bg-neutral-50 p-4 rounded-lg">
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-medium text-neutral-700">{dimension}</span>
                                        <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(score)}`}>
                                            {score.toFixed(2)}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* FDAC Analysis */}
                <div className="card mb-8">
                    <h2 className="text-2xl font-bold text-neutral-900 mb-6">FDAC - Análise de Cultura Organizacional</h2>
                    <div className="grid md:grid-cols-2 gap-4">
                        {Object.entries(analytics.fdac_dimensions).map(([dimension, score]) => (
                            <div key={dimension} className="bg-neutral-50 p-4 rounded-lg">
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-sm font-medium text-neutral-700">{dimension}</span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(score)}`}>
                                        {score.toFixed(2)}
                                    </span>
                                </div>
                                <div className="w-full bg-neutral-200 rounded-full h-2">
                                    <div
                                        className={`h-2 rounded-full ${score >= 4 ? 'bg-green-500' : score >= 3 ? 'bg-yellow-500' : 'bg-red-500'}`}
                                        style={{ width: `${(score / 5) * 100}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Department Breakdown */}
                {analytics.department_stats.length > 0 && (
                    <div className="card mb-8">
                        <h2 className="text-2xl font-bold text-neutral-900 mb-6">Análise por Departamento</h2>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="border-b border-neutral-200">
                                        <th className="text-left py-3 px-4 font-semibold text-neutral-700">Departamento</th>
                                        <th className="text-center py-3 px-4 font-semibold text-neutral-700">Respostas</th>
                                        <th className="text-center py-3 px-4 font-semibold text-neutral-700">IMCO Médio</th>
                                        <th className="text-center py-3 px-4 font-semibold text-neutral-700">FDAC Médio</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {analytics.department_stats.map((dept, idx) => (
                                        <tr key={idx} className="border-b border-neutral-100 hover:bg-neutral-50 transition">
                                            <td className="py-3 px-4 font-medium text-neutral-900">{dept.department_name}</td>
                                            <td className="py-3 px-4 text-center text-neutral-900">{dept.response_count}</td>
                                            <td className="py-3 px-4 text-center">
                                                <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(dept.imco_average)}`}>
                                                    {dept.imco_average.toFixed(2)}
                                                </span>
                                            </td>
                                            <td className="py-3 px-4 text-center">
                                                <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(dept.fdac_average)}`}>
                                                    {dept.fdac_average.toFixed(2)}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* Recent Responses */}
                <div className="card">
                    <h2 className="text-2xl font-bold text-neutral-900 mb-6">Respostas Recentes</h2>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-neutral-200">
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Departamento</th>
                                    <th className="text-center py-3 px-4 font-semibold text-neutral-700">IMCO</th>
                                    <th className="text-center py-3 px-4 font-semibold text-neutral-700">FDAC</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Data</th>
                                    <th className="text-center py-3 px-4 font-semibold text-neutral-700">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {analytics.recent_responses.map((response) => (
                                    <tr key={response.id} className="border-b border-neutral-100 hover:bg-neutral-50 transition">
                                        <td className="py-3 px-4 text-neutral-900">{response.department_name || 'Sem departamento'}</td>
                                        <td className="py-3 px-4 text-center">
                                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(response.imco_overall)}`}>
                                                {response.imco_overall.toFixed(2)}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4 text-center">
                                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskColor(response.fdac_overall)}`}>
                                                {response.fdac_overall.toFixed(2)}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4 text-neutral-600 text-sm">
                                            {new Date(response.completed_at).toLocaleString('pt-BR')}
                                        </td>
                                        <td className="py-3 px-4 text-center">
                                            <button
                                                onClick={() => loadResponseDetail(response.id)}
                                                className="text-primary-900 hover:text-primary-700 transition text-sm font-medium flex items-center mx-auto"
                                            >
                                                <Eye className="h-4 w-4 mr-1" />
                                                Ver Detalhes
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* Individual Response Modal */}
            {selectedResponse && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6 overflow-y-auto">
                    <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full p-6 my-8">
                        <div className="flex justify-between items-start mb-6">
                            <h3 className="text-2xl font-bold text-neutral-900">Resposta Individual</h3>
                            <button
                                onClick={() => setSelectedResponse(null)}
                                className="text-neutral-500 hover:text-neutral-700 text-2xl"
                            >
                                ×
                            </button>
                        </div>

                        {loadingResponse ? (
                            <div className="flex justify-center py-8">
                                <Loader2 className="h-8 w-8 animate-spin text-primary-900" />
                            </div>
                        ) : (
                            <div className="space-y-6">
                                {/* Info */}
                                <div className="grid md:grid-cols-2 gap-4 p-4 bg-neutral-50 rounded-lg">
                                    <div>
                                        <p className="text-sm text-neutral-600">Departamento</p>
                                        <p className="font-medium text-neutral-900">{selectedResponse.department_name || 'Não informado'}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm text-neutral-600">Data de Conclusão</p>
                                        <p className="font-medium text-neutral-900">
                                            {new Date(selectedResponse.completed_at).toLocaleString('pt-BR')}
                                        </p>
                                    </div>
                                </div>

                                {/* IMCO Details */}
                                <div>
                                    <h4 className="text-lg font-bold text-neutral-900 mb-3">IMCO - Clima Organizacional</h4>
                                    <div className="grid md:grid-cols-3 gap-4">
                                        <div className="p-4 bg-neutral-50 rounded-lg text-center">
                                            <p className="text-sm text-neutral-600 mb-1">Score Geral</p>
                                            <p className="text-2xl font-bold text-neutral-900">{selectedResponse.imco.overall.toFixed(2)}</p>
                                        </div>
                                        {Object.entries(selectedResponse.imco.vectors).slice(0, 2).map(([vector, score]) => (
                                            <div key={vector} className="p-4 bg-neutral-50 rounded-lg text-center">
                                                <p className="text-sm text-neutral-600 mb-1">{vector}</p>
                                                <p className="text-2xl font-bold text-neutral-900">{score.toFixed(2)}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* FDAC Details */}
                                <div>
                                    <h4 className="text-lg font-bold text-neutral-900 mb-3">FDAC - Cultura Organizacional</h4>
                                    <div className="grid md:grid-cols-3 gap-4">
                                        <div className="p-4 bg-neutral-50 rounded-lg text-center">
                                            <p className="text-sm text-neutral-600 mb-1">Score Geral</p>
                                            <p className="text-2xl font-bold text-neutral-900">{selectedResponse.fdac.overall.toFixed(2)}</p>
                                        </div>
                                        {Object.entries(selectedResponse.fdac.dimensions).slice(0, 2).map(([dimension, score]) => (
                                            <div key={dimension} className="p-4 bg-neutral-50 rounded-lg text-center">
                                                <p className="text-sm text-neutral-600 mb-1">{dimension}</p>
                                                <p className="text-2xl font-bold text-neutral-900">{score.toFixed(2)}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="pt-4 border-t border-neutral-200">
                                    <p className="text-sm text-neutral-600 italic">
                                        Total de {Object.keys(selectedResponse.answers).length} respostas coletadas nesta avaliação.
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}
