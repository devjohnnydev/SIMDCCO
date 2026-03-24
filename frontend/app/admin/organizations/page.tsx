"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, Building2, Plus, Edit, Trash2, ArrowLeft, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import { apiService } from '@/lib/api'
import AdminSidebar from '@/components/AdminSidebar'

interface Organization {
    id: string
    razao_social: string
    nome_fantasia: string | null
    created_at: string
}

export default function OrganizationsPage() {
    const router = useRouter()
    const [organizations, setOrganizations] = useState<Organization[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [showModal, setShowModal] = useState(false)
    const [editingOrg, setEditingOrg] = useState<Organization | null>(null)
    const [formData, setFormData] = useState({
        cnpj: '',
        razao_social: '',
        nome_fantasia: ''
    })
    const [submitting, setSubmitting] = useState(false)
    const [success, setSuccess] = useState('')

    useEffect(() => {
        loadOrganizations()
    }, [])

    const loadOrganizations = async () => {
        try {
            const response = await apiService.getOrganizations()
            setOrganizations(response.data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao carregar organizações')
        } finally {
            setLoading(false)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setSubmitting(true)
        setError('')

        try {
            if (editingOrg) {
                await apiService.updateOrganization(editingOrg.id, {
                    razao_social: formData.razao_social,
                    nome_fantasia: formData.nome_fantasia || undefined
                })
                setSuccess('Organização atualizada com sucesso!')
            } else {
                await apiService.createOrganization(formData)
                setSuccess('Organização criada com sucesso!')
            }

            setShowModal(false)
            setFormData({ cnpj: '', razao_social: '', nome_fantasia: '' })
            setEditingOrg(null)
            loadOrganizations()

            setTimeout(() => setSuccess(''), 3000)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao salvar organização')
        } finally {
            setSubmitting(false)
        }
    }

    const handleEdit = (org: Organization) => {
        setEditingOrg(org)
        setFormData({
            cnpj: '',
            razao_social: org.razao_social,
            nome_fantasia: org.nome_fantasia || ''
        })
        setShowModal(true)
    }

    const handleDelete = async (org: Organization) => {
        if (!confirm(`Tem certeza que deseja excluir "${org.razao_social}"?`)) return

        try {
            await apiService.deleteOrganization(org.id)
            setSuccess('Organização excluída com sucesso!')
            loadOrganizations()
            setTimeout(() => setSuccess(''), 3000)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao excluir organização')
        }
    }

    const openCreateModal = () => {
        setEditingOrg(null)
        setFormData({ cnpj: '', razao_social: '', nome_fantasia: '' })
        setShowModal(true)
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="h-12 w-12 animate-spin text-primary-900" />
            </div>
        )
    }

    return (
        <div className="flex min-h-screen bg-neutral-50">
            <AdminSidebar />

            <div className="flex-1 ml-64">
                <div className="container mx-auto px-6 py-8">
                    {/* Success/Error Messages */}
                    {success && (
                        <div className="alert-success mb-6 flex items-center">
                            <CheckCircle className="h-5 w-5 mr-2" />
                            {success}
                        </div>
                    )}

                    {error && (
                        <div className="alert-danger mb-6 flex items-center">
                            <AlertCircle className="h-5 w-5 mr-2" />
                            {error}
                        </div>
                    )}

                    {/* Header Actions */}
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold text-neutral-900">
                            Empresas Cadastradas ({organizations.length})
                        </h2>
                        <button onClick={openCreateModal} className="btn-primary flex items-center">
                            <Plus className="h-5 w-5 mr-2" />
                            Nova Organização
                        </button>
                    </div>

                    {/* Organizations Table */}
                    <div className="card">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-neutral-200">
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Razão Social</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Nome Fantasia</th>
                                    <th className="text-left py-3 px-4 font-semibold text-neutral-700">Criado em</th>
                                    <th className="text-right py-3 px-4 font-semibold text-neutral-700">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {organizations.length === 0 ? (
                                    <tr>
                                        <td colSpan={4} className="text-center py-8 text-neutral-500">
                                            Nenhuma organização cadastrada
                                        </td>
                                    </tr>
                                ) : (
                                    organizations.map(org => (
                                        <tr key={org.id} className="border-b border-neutral-100 hover:bg-neutral-50 transition">
                                            <td className="py-3 px-4 font-medium text-neutral-900">{org.razao_social}</td>
                                            <td className="py-3 px-4 text-neutral-600">{org.nome_fantasia || '-'}</td>
                                            <td className="py-3 px-4 text-neutral-600 text-sm">
                                                {new Date(org.created_at).toLocaleDateString('pt-BR')}
                                            </td>
                                            <td className="py-3 px-4 text-right">
                                                <button
                                                    onClick={() => handleEdit(org)}
                                                    className="text-primary-900 hover:text-primary-700 mr-3 transition"
                                                >
                                                    <Edit className="h-4 w-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(org)}
                                                    className="text-danger-700 hover:text-danger-900 transition"
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Modal */}
                {showModal && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
                        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6 animate-fade-in">
                            <h3 className="text-xl font-bold text-neutral-900 mb-6">
                                {editingOrg ? 'Editar Organização' : 'Nova Organização'}
                            </h3>

                            <form onSubmit={handleSubmit} className="space-y-4">
                                {!editingOrg && (
                                    <div>
                                        <label className="block text-sm font-medium text-neutral-700 mb-2">
                                            CNPJ *
                                        </label>
                                        <input
                                            type="text"
                                            className="input"
                                            placeholder="00.000.000/0000-00"
                                            value={formData.cnpj}
                                            onChange={(e) => setFormData({ ...formData, cnpj: e.target.value })}
                                            required
                                            maxLength={18}
                                        />
                                    </div>
                                )}

                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Razão Social *
                                    </label>
                                    <input
                                        type="text"
                                        className="input"
                                        placeholder="Nome da empresa"
                                        value={formData.razao_social}
                                        onChange={(e) => setFormData({ ...formData, razao_social: e.target.value })}
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Nome Fantasia
                                    </label>
                                    <input
                                        type="text"
                                        className="input"
                                        placeholder="Nome popular (opcional)"
                                        value={formData.nome_fantasia}
                                        onChange={(e) => setFormData({ ...formData, nome_fantasia: e.target.value })}
                                    />
                                </div>

                                <div className="flex space-x-3 pt-4">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="btn-outline flex-1"
                                        disabled={submitting}
                                    >
                                        Cancelar
                                    </button>
                                    <button
                                        type="submit"
                                        className="btn-primary flex-1"
                                        disabled={submitting}
                                    >
                                        {submitting ? (
                                            <>
                                                <Loader2 className="h-4 w-4 mr-2 animate-spin inline" />
                                                Salvando...
                                            </>
                                        ) : (
                                            editingOrg ? 'Atualizar' : 'Criar'
                                        )}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

