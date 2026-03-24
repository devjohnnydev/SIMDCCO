"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, Plus, Calendar, Users, CheckCircle, XCircle, Copy, ArrowLeft, Loader2, BarChart3 } from 'lucide-react'
import { apiService } from '@/lib/api'

export default function CampaignsPage() {
    const router = useRouter()
    const [campaigns, setCampaigns] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [showCreateModal, setShowCreateModal] = useState(false)
    const [creating, setCreating] = useState(false)
    const [organizations, setOrganizations] = useState<any[]>([])
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        start_date: new Date().toISOString().split('T')[0],
        end_date: '',
        organization_id: ''
    })

    useEffect(() => {
        loadCampaigns()
        loadOrganizations()
    }, [])

    const loadOrganizations = async () => {
        try {
            const response = await apiService.getOrganizations()
            setOrganizations(response.data)
            if (response.data.length > 0) {
                setFormData(prev => ({ ...prev, organization_id: response.data[0].id }))
            }
        } catch (error) {
            console.error('Error loading organizations:', error)
        }
    }

    const loadCampaigns = async () => {
        try {
            const response = await apiService.getCampaigns()
            setCampaigns(response.data)
        } catch (error: any) {
            if (error.response?.status === 401) {
                router.push('/admin/login')
            }
        } finally {
            setLoading(false)
        }
    }

    const handleCreateCampaign = async (e: React.FormEvent) => {
        e.preventDefault()
        setCreating(true)

        try {
            await apiService.createCampaign({
                name: formData.name,
                description: formData.description,
                start_date: new Date(formData.start_date).toISOString(),
                end_date: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
                organization_id: formData.organization_id || undefined
            })

            setShowCreateModal(false)
            setFormData({
                name: '',
                description: '',
                start_date: new Date().toISOString().split('T')[0],
                end_date: '',
                organization_id: organizations.length > 0 ? organizations[0].id : ''
            })
            loadCampaigns()
        } catch (error) {
            alert('Erro ao criar campanha')
        } finally {
            setCreating(false)
        }
    }

    const handleToggleCampaign = async (id: string) => {
        try {
            await apiService.toggleCampaign(id)
            loadCampaigns()
        } catch (error) {
            alert('Erro ao atualizar campanha')
        }
    }

    const copyLink = (slug: string) => {
        const link = `${window.location.origin}/respondent?c=${slug}`
        navigator.clipboard.writeText(link)
        alert('Link copiado para a área de transferência!')
    }

    const openCreateModal = () => {
        loadOrganizations()
        setShowCreateModal(true)
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100">
            {/* Header */}
            <nav className="bg-white border-b border-neutral-200 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <Link href="/admin/dashboard" className="flex items-center space-x-2">
                                <Shield className="h-8 w-8 text-primary-900" />
                                <span className="text-2xl font-bold text-primary-900">SIMDCCO</span>
                            </Link>
                            <span className="text-neutral-300">/</span>
                            <span className="text-neutral-700">Campanhas</span>
                        </div>
                        <Link href="/admin/dashboard" className="btn-outline">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Dashboard
                        </Link>
                    </div>
                </div>
            </nav>

            <div className="container mx-auto px-6 py-12">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-neutral-900 mb-2">
                            Gestão de Campanhas
                        </h1>
                        <p className="text-neutral-600">
                            Crie e gerencie campanhas de diagnóstico organizacional
                        </p>
                    </div>
                    <button
                        onClick={openCreateModal}
                        className="btn-primary flex items-center"
                    >
                        <Plus className="h-5 w-5 mr-2" />
                        Nova Campanha
                    </button>
                </div>

                {loading ? (
                    <div className="text-center py-12">
                        <Loader2 className="h-12 w-12 animate-spin text-primary-900 mx-auto mb-4" />
                        <p className="text-neutral-600">Carregando campanhas...</p>
                    </div>
                ) : campaigns.length === 0 ? (
                    <div className="card-premium text-center py-16">
                        <Calendar className="h-16 w-16 text-neutral-300 mx-auto mb-6" />
                        <h2 className="text-2xl font-bold text-neutral-900 mb-4">
                            Nenhuma campanha criada
                        </h2>
                        <p className="text-neutral-600 mb-8 max-w-md mx-auto">
                            Campanhas organizam a coleta de respostas e permitem gerar links únicos
                            para enviar aos respondentes.
                        </p>
                        <button
                            onClick={openCreateModal}
                            className="btn-primary inline-flex items-center"
                        >
                            <Plus className="h-5 w-5 mr-2" />
                            Criar Primeira Campanha
                        </button>
                    </div>
                ) : (
                    <div className="grid gap-6">
                        {campaigns.map((campaign) => (
                            <div key={campaign.id} className="card-premium hover-lift">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-3 mb-2">
                                            <h3 className="text-xl font-bold text-neutral-900">
                                                {campaign.name}
                                            </h3>
                                            {campaign.is_active ? (
                                                <span className="badge-low flex items-center">
                                                    <CheckCircle className="h-3 w-3 mr-1" />
                                                    Ativa
                                                </span>
                                            ) : (
                                                <span className="px-3 py-1 bg-neutral-200 text-neutral-700 rounded-full text-sm font-medium flex items-center">
                                                    <XCircle className="h-3 w-3 mr-1" />
                                                    Inativa
                                                </span>
                                            )}
                                        </div>
                                        {campaign.description && (
                                            <p className="text-neutral-600 mb-4">{campaign.description}</p>
                                        )}
                                        <div className="flex items-center space-x-6 text-sm text-neutral-500">
                                            <span className="flex items-center">
                                                <Calendar className="h-4 w-4 mr-1" />
                                                Início: {new Date(campaign.start_date).toLocaleDateString('pt-BR')}
                                            </span>
                                            <span className="flex items-center">
                                                <Users className="h-4 w-4 mr-1" />
                                                {campaign.response_count} respostas
                                            </span>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => handleToggleCampaign(campaign.id)}
                                        className={`px-4 py-2 rounded-lg font-medium transition ${campaign.is_active
                                            ? 'bg-neutral-200 text-neutral-700 hover:bg-neutral-300'
                                            : 'bg-secondary-700 text-white hover:bg-secondary-500'
                                            }`}
                                    >
                                        {campaign.is_active ? 'Desativar' : 'Ativar'}
                                    </button>
                                </div>

                                <div className="border-t border-neutral-200 pt-4">
                                    <div className="flex items-center justify-between">
                                        <div className="flex-1">
                                            <p className="text-xs text-neutral-500 mb-1">Link da Campanha:</p>
                                            <code className="text-sm bg-neutral-100 px-3 py-2 rounded block">
                                                {typeof window !== 'undefined' ? window.location.origin : ''}/respondent?c={campaign.slug}
                                            </code>
                                        </div>
                                        <button
                                            onClick={() => copyLink(campaign.slug)}
                                            className="ml-4 btn-outline flex items-center"
                                        >
                                            <Copy className="h-4 w-4 mr-2" />
                                            Copiar Link
                                        </button>
                                        <Link
                                            href={`/admin/campaigns/${campaign.id}/analytics`}
                                            className="ml-4 btn-primary flex items-center"
                                        >
                                            <BarChart3 className="h-4 w-4 mr-2" />
                                            Ver Analytics
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Create Campaign Modal */}
            {showCreateModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
                    <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="p-8">
                            <h2 className="text-2xl font-bold text-neutral-900 mb-6">
                                Criar Nova Campanha
                            </h2>

                            <form onSubmit={handleCreateCampaign} className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Organização *
                                    </label>
                                    <select
                                        className="input"
                                        required
                                        value={formData.organization_id}
                                        onChange={(e) => setFormData({ ...formData, organization_id: e.target.value })}
                                    >
                                        {organizations.map(org => (
                                            <option key={org.id} value={org.id}>
                                                {org.razao_social}
                                            </option>
                                        ))}
                                    </select>
                                    {organizations.length === 0 && (
                                        <p className="text-xs text-secondary-700 mt-1">
                                            ⚠️ Nenhuma organização cadastrada. Crie uma primeiro no menu Organizações.
                                        </p>
                                    )}
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Nome da Campanha *
                                    </label>
                                    <input
                                        type="text"
                                        className="input"
                                        required
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        placeholder="Ex: Diagnóstico Q1 2026"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Descrição
                                    </label>
                                    <textarea
                                        className="input min-h-[100px]"
                                        value={formData.description}
                                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                        placeholder="Descreva o objetivo desta campanha..."
                                    />
                                </div>

                                <div className="grid md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-medium text-neutral-700 mb-2">
                                            Data de Início *
                                        </label>
                                        <input
                                            type="date"
                                            className="input"
                                            required
                                            value={formData.start_date}
                                            onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-neutral-700 mb-2">
                                            Data de Término (Opcional)
                                        </label>
                                        <input
                                            type="date"
                                            className="input"
                                            value={formData.end_date}
                                            onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div className="bg-primary-900 bg-opacity-5 border border-primary-900 border-opacity-20 p-4 rounded-lg">
                                    <p className="text-sm text-neutral-700">
                                        💡 <strong>Dica:</strong> Após criar a campanha, você receberá um link único
                                        que pode ser compartilhado com os respondentes via e-mail, WhatsApp ou
                                        QR Code.
                                    </p>
                                </div>

                                <div className="flex items-center space-x-4 pt-4">
                                    <button
                                        type="submit"
                                        disabled={creating}
                                        className="btn-primary flex-1 flex items-center justify-center disabled:opacity-50"
                                    >
                                        {creating ? (
                                            <>
                                                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                                                Criando...
                                            </>
                                        ) : (
                                            <>
                                                <Plus className="h-5 w-5 mr-2" />
                                                Criar Campanha
                                            </>
                                        )}
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setShowCreateModal(false)}
                                        className="btn-outline flex-1"
                                        disabled={creating}
                                    >
                                        Cancelar
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
