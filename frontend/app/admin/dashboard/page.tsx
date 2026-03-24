"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, BarChart3, Users, TrendingUp, AlertTriangle, CheckCircle, Calendar, Plus, Building2 } from 'lucide-react'
import { apiService } from '@/lib/api'
import AdminSidebar from '@/components/AdminSidebar'

interface Analytics {
    respondent_count: number
    imco_scores: {
        overall: number
        vectors: Record<string, number>
        dimensions: Record<string, number>
    }
    fdac_scores: {
        overall: number
        dimensions: Record<string, number>
    }
    risk_level: string
}

export default function AdminDashboard() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)
    const [analytics, setAnalytics] = useState<Analytics | null>(null)
    const [campaigns, setCampaigns] = useState<any[]>([])

    useEffect(() => {
        loadDashboardData()
    }, [])

    const loadDashboardData = async () => {
        try {
            // Load analytics
            const analyticsRes = await apiService.getOrganizationAnalytics()
            setAnalytics(analyticsRes.data)

            // Load campaigns
            const campaignsRes = await apiService.getCampaigns()
            setCampaigns(campaignsRes.data)
        } catch (error: any) {
            if (error.response?.status === 401) {
                router.push('/admin/login')
            }
        } finally {
            setLoading(false)
        }
    }

    const getRiskBadgeClass = (risk: string) => {
        switch (risk) {
            case 'low': return 'badge-low'
            case 'medium': return 'badge-medium'
            case 'high':
            case 'critical': return 'badge-high'
            default: return 'badge-medium'
        }
    }

    const getRiskLabel = (risk: string) => {
        const labels: Record<string, string> = {
            low: 'Baixo Risco',
            medium: 'Médio Risco',
            high: 'Alto Risco',
            critical: 'Risco Crítico'
        }
        return labels[risk] || risk
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-900 mx-auto mb-4"></div>
                    <p className="text-neutral-600">Carregando dashboard...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="flex min-h-screen bg-neutral-50">
            <AdminSidebar />

            <div className="flex-1 ml-64">
                {/* Content */}
                <div className="container mx-auto px-6 py-12">
                    <h1 className="text-3xl font-bold text-neutral-900 mb-8">
                        Dashboard Executivo
                    </h1>

                    {/* KPI Cards */}
                    <div className="grid md:grid-cols-4 gap-6 mb-12">
                        <div className="card hover-lift">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-primary-900 bg-opacity-10 rounded-lg">
                                    <Users className="h-6 w-6 text-primary-900" />
                                </div>
                            </div>
                            <p className="text-sm text-neutral-600 mb-1">Respondentes</p>
                            <p className="text-3xl font-bold text-neutral-900">
                                {analytics?.respondent_count || 0}
                            </p>
                        </div>

                        <div className="card hover-lift">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-secondary-700 bg-opacity-10 rounded-lg">
                                    <TrendingUp className="h-6 w-6 text-secondary-700" />
                                </div>
                            </div>
                            <p className="text-sm text-neutral-600 mb-1">Clima (IMCO)</p>
                            <p className="text-3xl font-bold text-neutral-900">
                                {analytics?.imco_scores?.overall?.toFixed(1) || '-'}
                            </p>
                        </div>

                        <div className="card hover-lift">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-secondary-700 bg-opacity-10 rounded-lg">
                                    <BarChart3 className="h-6 w-6 text-secondary-700" />
                                </div>
                            </div>
                            <p className="text-sm text-neutral-600 mb-1">Cultura (FDAC)</p>
                            <p className="text-3xl font-bold text-neutral-900">
                                {analytics?.fdac_scores?.overall?.toFixed(1) || '-'}
                            </p>
                        </div>

                        <div className="card hover-lift">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-warning-500 bg-opacity-10 rounded-lg">
                                    <AlertTriangle className="h-6 w-6 text-warning-500" />
                                </div>
                            </div>
                            <p className="text-sm text-neutral-600 mb-1">Nível de Risco</p>
                            <span className={`${getRiskBadgeClass(analytics?.risk_level || 'low')} text-sm`}>
                                {getRiskLabel(analytics?.risk_level || 'low')}
                            </span>
                        </div>
                    </div>

                    {/* IMCO Vectors */}
                    {analytics?.imco_scores?.vectors && (
                        <div className="card-premium mb-8">
                            <h2 className="text-xl font-bold text-neutral-900 mb-6">
                                Vetores IMCO - Clima Organizacional
                            </h2>
                            <div className="space-y-4">
                                {Object.entries(analytics.imco_scores.vectors).map(([vector, score]) => (
                                    <div key={vector}>
                                        <div className="flex justify-between mb-2">
                                            <span className="text-sm font-medium text-neutral-700">{vector}</span>
                                            <span className="text-sm font-bold text-neutral-900">{score.toFixed(1)}</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-fill"
                                                style={{ width: `${(score / 5) * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* FDAC Dimensions */}
                    {analytics?.fdac_scores?.dimensions && (
                        <div className="card-premium mb-8">
                            <h2 className="text-xl font-bold text-neutral-900 mb-6">
                                Dimensões FDAC - Cultura Organizacional
                            </h2>
                            <div className="grid md:grid-cols-2 gap-6">
                                {Object.entries(analytics.fdac_scores.dimensions).map(([dimension, score]) => (
                                    <div key={dimension} className="bg-neutral-50 p-4 rounded-lg">
                                        <div className="flex justify-between items-center mb-2">
                                            <span className="font-medium text-neutral-900">{dimension}</span>
                                            <span className="text-2xl font-bold text-primary-900">{score.toFixed(1)}</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-fill"
                                                style={{ width: `${(score / 5) * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Campaigns */}
                    <div className="card-premium">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-bold text-neutral-900">
                                Campanhas Recentes
                            </h2>
                            <Link href="/admin/campaigns" className="btn-primary flex items-center">
                                <Plus className="h-4 w-4 mr-2" />
                                Nova Campanha
                            </Link>
                        </div>

                        {campaigns.length === 0 ? (
                            <div className="text-center py-12">
                                <Calendar className="h-12 w-12 text-neutral-300 mx-auto mb-4" />
                                <p className="text-neutral-600 mb-4">Nenhuma campanha criada ainda</p>
                                <Link href="/admin/campaigns" className="btn-primary inline-flex items-center">
                                    <Plus className="h-4 w-4 mr-2" />
                                    Criar Primeira Campanha
                                </Link>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {campaigns.slice(0, 5).map((campaign) => (
                                    <div key={campaign.id} className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg hover-lift">
                                        <div className="flex-1">
                                            <h3 className="font-semibold text-neutral-900">{campaign.name}</h3>
                                            <p className="text-sm text-neutral-600">
                                                {campaign.response_count} respostas
                                            </p>
                                        </div>
                                        <div className="flex items-center space-x-4">
                                            {campaign.is_active ? (
                                                <span className="badge-low flex items-center">
                                                    <CheckCircle className="h-3 w-3 mr-1" />
                                                    Ativa
                                                </span>
                                            ) : (
                                                <span className="text-sm text-neutral-500">Inativa</span>
                                            )}
                                            <Link
                                                href={`/admin/campaigns/${campaign.id}/analytics`}
                                                className="text-primary-900 hover:text-primary-700 text-sm font-medium"
                                            >
                                                Ver detalhes →
                                            </Link>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}


