"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Shield, Mail, Phone, Building2, User, ArrowLeft, Loader2, AlertCircle, Calendar, MessageSquare } from 'lucide-react'
import { apiService } from '@/lib/api'

interface DemoLead {
    id: string
    nome: string
    email: string
    telefone: string
    empresa: string
    cargo: string | null
    mensagem: string | null
    created_at: string
}

export default function DemoLeadsPage() {
    const [leads, setLeads] = useState<DemoLead[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedLead, setSelectedLead] = useState<DemoLead | null>(null)

    useEffect(() => {
        loadLeads()
    }, [])

    const loadLeads = async () => {
        try {
            const response = await apiService.getDemoLeads()
            setLeads(response.data.leads)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao carregar leads')
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="h-12 w-12 animate-spin text-primary-900" />
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
                            <h1 className="text-xl font-semibold text-neutral-900">Leads de Demonstração</h1>
                        </div>
                        <Link href="/admin/dashboard" className="btn-outline flex items-center">
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

                {/* Stats */}
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                    <div className="card">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-neutral-600 mb-1">Total de Leads</p>
                                <p className="text-3xl font-bold text-neutral-900">{leads.length}</p>
                            </div>
                            <Mail className="h-12 w-12 text-primary-900 opacity-20" />
                        </div>
                    </div>
                    <div className="card">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-neutral-600 mb-1">Últimos 7 dias</p>
                                <p className="text-3xl font-bold text-neutral-900">
                                    {leads.filter(l => {
                                        const weekAgo = new Date()
                                        weekAgo.setDate(weekAgo.getDate() - 7)
                                        return new Date(l.created_at) > weekAgo
                                    }).length}
                                </p>
                            </div>
                            <Calendar className="h-12 w-12 text-secondary-700 opacity-20" />
                        </div>
                    </div>
                    <div className="card">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-neutral-600 mb-1">Empresas Únicas</p>
                                <p className="text-3xl font-bold text-neutral-900">
                                    {new Set(leads.map(l => l.empresa)).size}
                                </p>
                            </div>
                            <Building2 className="h-12 w-12 text-primary-900 opacity-20" />
                        </div>
                    </div>
                </div>

                {/* Leads Table */}
                <div className="card">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-neutral-200">
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Nome</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Empresa</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">E-mail</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Telefone</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Data</th>
                                    <th className="text-center py-3 px-4 font-semibold text-neutral-700">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {leads.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="text-center py-8 text-neutral-500">
                                            Nenhum lead cadastrado ainda
                                        </td>
                                    </tr>
                                ) : (
                                    leads.map(lead => (
                                        <tr key={lead.id} className="border-b border-neutral-100 hover:bg-neutral-50 transition">
                                            <td className="py-3 px-4">
                                                <div className="font-medium text-neutral-900">{lead.nome}</div>
                                                {lead.cargo && (
                                                    <div className="text-xs text-neutral-500">{lead.cargo}</div>
                                                )}
                                            </td>
                                            <td className="py-3 px-4 text-neutral-900">{lead.empresa}</td>
                                            <td className="py-3 px-4">
                                                <a href={`mailto:${lead.email}`} className="text-primary-900 hover:underline">
                                                    {lead.email}
                                                </a>
                                            </td>
                                            <td className="py-3 px-4 text-neutral-600">{lead.telefone}</td>
                                            <td className="py-3 px-4 text-neutral-600 text-sm">
                                                {new Date(lead.created_at).toLocaleString('pt-BR')}
                                            </td>
                                            <td className="py-3 px-4 text-center">
                                                <button
                                                    onClick={() => setSelectedLead(lead)}
                                                    className="text-primary-900 hover:text-primary-700 transition text-sm font-medium"
                                                >
                                                    Ver Detalhes
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* Detail Modal */}
            {selectedLead && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
                    <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6 animate-fade-in">
                        <div className="flex justify-between items-start mb-6">
                            <h3 className="text-2xl font-bold text-neutral-900">Detalhes do Lead</h3>
                            <button
                                onClick={() => setSelectedLead(null)}
                                className="text-neutral-500 hover:text-neutral-700"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 flex items-center mb-1">
                                        <User className="h-4 w-4 mr-2" />
                                        Nome
                                    </label>
                                    <p className="text-neutral-900">{selectedLead.nome}</p>
                                </div>
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 flex items-center mb-1">
                                        <Building2 className="h-4 w-4 mr-2" />
                                        Empresa
                                    </label>
                                    <p className="text-neutral-900">{selectedLead.empresa}</p>
                                </div>
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 flex items-center mb-1">
                                        <Mail className="h-4 w-4 mr-2" />
                                        E-mail
                                    </label>
                                    <a href={`mailto:${selectedLead.email}`} className="text-primary-900 hover:underline">
                                        {selectedLead.email}
                                    </a>
                                </div>
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 flex items-center mb-1">
                                        <Phone className="h-4 w-4 mr-2" />
                                        Telefone
                                    </label>
                                    <a href={`tel:${selectedLead.telefone}`} className="text-primary-900 hover:underline">
                                        {selectedLead.telefone}
                                    </a>
                                </div>
                            </div>

                            {selectedLead.cargo && (
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 mb-1 block">Cargo</label>
                                    <p className="text-neutral-900">{selectedLead.cargo}</p>
                                </div>
                            )}

                            {selectedLead.mensagem && (
                                <div>
                                    <label className="text-sm font-medium text-neutral-600 flex items-center mb-2">
                                        <MessageSquare className="h-4 w-4 mr-2" />
                                        Mensagem
                                    </label>
                                    <div className="bg-neutral-50 p-4 rounded-lg">
                                        <p className="text-neutral-900 whitespace-pre-wrap">{selectedLead.mensagem}</p>
                                    </div>
                                </div>
                            )}

                            <div className="pt-4 border-t border-neutral-200">
                                <label className="text-sm font-medium text-neutral-600 flex items-center mb-1">
                                    <Calendar className="h-4 w-4 mr-2" />
                                    Data da Solicitação
                                </label>
                                <p className="text-neutral-900">{new Date(selectedLead.created_at).toLocaleString('pt-BR')}</p>
                            </div>
                        </div>

                        <div className="mt-6 flex space-x-3">
                            <a
                                href={`mailto:${selectedLead.email}`}
                                className="btn-primary flex-1 text-center"
                            >
                                <Mail className="h-4 w-4 mr-2 inline" />
                                Enviar E-mail
                            </a>
                            <a
                                href={`tel:${selectedLead.telefone}`}
                                className="btn-outline flex-1 text-center"
                            >
                                <Phone className="h-4 w-4 mr-2 inline" />
                                Ligar
                            </a>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
