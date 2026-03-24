"use client"

import { useState } from 'react'
import Link from 'next/link'
import { Shield, ArrowLeft, Send, CheckCircle, Building2, User, Mail, Phone, MessageSquare, Loader2, AlertCircle } from 'lucide-react'
import { apiService } from '@/lib/api'

export default function DemoPage() {
    const [submitted, setSubmitted] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [formData, setFormData] = useState({
        nome: '',
        email: '',
        telefone: '',
        empresa: '',
        cargo: '',
        mensagem: ''
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            await apiService.submitDemo(formData)
            setSubmitted(true)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao enviar solicitação. Tente novamente.')
        } finally {
            setLoading(false)
        }
    }

    if (submitted) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center px-6">
                <div className="max-w-2xl w-full">
                    <div className="card-premium text-center animate-fade-in">
                        <div className="inline-flex items-center justify-center w-24 h-24 bg-secondary-700 bg-opacity-10 rounded-full mb-8">
                            <CheckCircle className="h-12 w-12 text-secondary-700" />
                        </div>

                        <h1 className="text-3xl font-bold text-neutral-900 mb-4">
                            Solicitação Enviada com Sucesso!
                        </h1>

                        <p className="text-lg text-neutral-600 mb-8">
                            Obrigado pelo seu interesse no SIMDCCO. Nossa equipe entrará em contato
                            em até 24 horas para agendar sua demonstração personalizada.
                        </p>

                        <div className="bg-primary-900 bg-opacity-5 border border-primary-900 border-opacity-20 p-6 rounded-lg mb-8">
                            <h3 className="font-semibold text-neutral-900 mb-3">O que acontece agora?</h3>
                            <ul className="text-left text-neutral-700 space-y-2">
                                <li>✓ Análise do seu caso pela equipe técnica</li>
                                <li>✓ Agendamento de demonstração ao vivo</li>
                                <li>✓ Apresentação de proposta customizada</li>
                                <li>✓ Suporte completo para implementação</li>
                            </ul>
                        </div>

                        <Link href="/" className="btn-primary inline-flex items-center">
                            <ArrowLeft className="h-5 w-5 mr-2" />
                            Voltar ao Início
                        </Link>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100">
            {/* Header */}
            <nav className="bg-white border-b border-neutral-200 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-2">
                            <Shield className="h-8 w-8 text-primary-900" />
                            <span className="text-2xl font-bold text-primary-900">SIMDCCO</span>
                        </Link>
                        <Link href="/" className="btn-outline">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Voltar
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Content */}
            <div className="container mx-auto px-6 py-12">
                <div className="max-w-3xl mx-auto">
                    {/* Header */}
                    <div className="text-center mb-12 animate-fade-in">
                        <h1 className="text-4xl font-bold text-neutral-900 mb-4">
                            Solicite uma Demonstração
                        </h1>
                        <p className="text-xl text-neutral-600">
                            Descubra como o SIMDCCO pode ajudar sua empresa a garantir compliance NR-01
                            e proteger-se juridicamente
                        </p>
                    </div>

                    {/* Benefits */}
                    <div className="grid md:grid-cols-3 gap-6 mb-12">
                        {[
                            { icon: '⚡', title: 'Implementação Rápida', desc: 'Sistema pronto em 48h' },
                            { icon: '🛡️', title: 'Garantia Legal', desc: 'Laudos com valor probatório' },
                            { icon: '📊', title: 'Análise Completa', desc: '100 questionários validados' }
                        ].map((item, idx) => (
                            <div key={idx} className="bg-white rounded-lg p-6 shadow-md text-center hover-lift">
                                <div className="text-4xl mb-3">{item.icon}</div>
                                <h3 className="font-semibold text-neutral-900 mb-2">{item.title}</h3>
                                <p className="text-sm text-neutral-600">{item.desc}</p>
                            </div>
                        ))}
                    </div>

                    {/* Form */}
                    <div className="card-premium animate-fade-in">
                        <h2 className="text-2xl font-bold text-neutral-900 mb-6">
                            Preencha seus dados
                        </h2>

                        {error && (
                            <div className="alert-danger mb-6 flex items-start">
                                <AlertCircle className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        <User className="inline h-4 w-4 mr-2" />
                                        Nome Completo *
                                    </label>
                                    <input
                                        type="text"
                                        className="input"
                                        required
                                        value={formData.nome}
                                        onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                                        placeholder="Seu nome"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        <Mail className="inline h-4 w-4 mr-2" />
                                        E-mail Corporativo *
                                    </label>
                                    <input
                                        type="email"
                                        className="input"
                                        required
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        placeholder="seu@empresa.com"
                                    />
                                </div>
                            </div>

                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        <Phone className="inline h-4 w-4 mr-2" />
                                        Telefone *
                                    </label>
                                    <input
                                        type="tel"
                                        className="input"
                                        required
                                        value={formData.telefone}
                                        onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                                        placeholder="(11) 99999-9999"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                                        Cargo
                                    </label>
                                    <input
                                        type="text"
                                        className="input"
                                        value={formData.cargo}
                                        onChange={(e) => setFormData({ ...formData, cargo: e.target.value })}
                                        placeholder="Ex: Gerente de RH"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <Building2 className="inline h-4 w-4 mr-2" />
                                    Empresa *
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    required
                                    value={formData.empresa}
                                    onChange={(e) => setFormData({ ...formData, empresa: e.target.value })}
                                    placeholder="Nome da empresa"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <MessageSquare className="inline h-4 w-4 mr-2" />
                                    Mensagem (Opcional)
                                </label>
                                <textarea
                                    className="input min-h-[120px]"
                                    value={formData.mensagem}
                                    onChange={(e) => setFormData({ ...formData, mensagem: e.target.value })}
                                    placeholder="Conte-nos um pouco sobre suas necessidades..."
                                />
                            </div>

                            <div className="bg-neutral-100 p-4 rounded-lg">
                                <p className="text-sm text-neutral-600">
                                    Ao enviar este formulário, você concorda em ser contatado pela equipe SIMDCCO
                                    para apresentação do sistema. Seus dados são protegidos conforme LGPD.
                                </p>
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="btn-primary w-full flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                                        Enviando...
                                    </>
                                ) : (
                                    <>
                                        <Send className="h-5 w-5 mr-2" />
                                        Solicitar Demonstração Gratuita
                                    </>
                                )}
                            </button>
                        </form>
                    </div>

                    {/* Trust Signals */}
                    <div className="mt-12 text-center">
                        <p className="text-sm text-neutral-500 mb-4">
                            Sistema idealizado por perito judicial | Compliance NR-01 | LGPD
                        </p>
                        <div className="flex items-center justify-center space-x-6 text-xs text-neutral-400">
                            <span>🔒 Dados Criptografados</span>
                            <span>⚖️ Valor Probatório</span>
                            <span>📊 100% Validado</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
