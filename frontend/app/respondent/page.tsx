"use client"

import { useState, Suspense } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { Shield, Loader2, AlertCircle, CheckCircle, Building2, User, Mail, Hash } from 'lucide-react'
import { apiService } from '@/lib/api'

function RespondentContent() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const campaignSlug = searchParams.get('c')

    const [step, setStep] = useState<'welcome' | 'validate' | 'consent'>('welcome')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const [formData, setFormData] = useState({
        cpf: '',
        email: '',
        cnpj: '',
        department_name: ''
    })

    const [validationResult, setValidationResult] = useState<any>(null)
    const [consentAccepted, setConsentAccepted] = useState(false)

    const handleValidation = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            // Validate with optional campaign slug
            const params = campaignSlug ? { campaign_slug: campaignSlug } : {}
            const response = await apiService.validateRespondent({
                cpf: formData.cpf,
                email: formData.email,
                cnpj: formData.cnpj,
                department_name: formData.department_name,
                ...params
            })
            setValidationResult(response.data)
            setStep('consent')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao validar dados. Verifique e tente novamente.')
        } finally {
            setLoading(false)
        }
    }

    const handleConsent = async () => {
        if (!consentAccepted || !validationResult) {
            setError('Você precisa aceitar os termos para continuar.')
            return
        }

        setLoading(true)
        setError('')

        try {
            // Register consent with optional campaign slug
            const params = campaignSlug ? { campaign_slug: campaignSlug } : {}
            const response = await apiService.registerConsent({
                cpf: formData.cpf,
                cnpj: formData.cnpj,
                email: formData.email,
                ...params
            })

            // Store session data including campaign slug
            sessionStorage.setItem('respondent_session', JSON.stringify({
                cpf: formData.cpf,
                cnpj: formData.cnpj,
                email: formData.email,
                department_id: validationResult.department_id,
                session_id: validationResult.session_id,
                campaign_slug: campaignSlug
            }))

            router.push('/respondent/questionnaire')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao registrar consentimento.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
            {/* Header */}
            <nav className="bg-white border-b border-neutral-200 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <Link href="/" className="flex items-center space-x-2">
                        <Shield className="h-8 w-8 text-primary-900" />
                        <span className="text-2xl font-bold text-primary-900">SIMDCCO</span>
                    </Link>
                </div>
            </nav>

            <div className="container mx-auto px-6 py-12 max-w-2xl">
                {/* Welcome Step */}
                {step === 'welcome' && (
                    <div className="card-premium animate-fade-in">
                        <div className="text-center mb-8">
                            <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-900 bg-opacity-10 rounded-full mb-6">
                                <Shield className="h-10 w-10 text-primary-900" />
                            </div>
                            <h1 className="text-3xl font-bold text-neutral-900 mb-4">
                                Bem-vindo ao Diagnóstico SIMDCCO
                            </h1>
                            <p className="text-lg text-neutral-600">
                                Sistema de Avaliação de Saúde Mental, Clima e Cultura Organizacional
                            </p>
                            {campaignSlug && (
                                <span className="inline-block mt-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                                    Campanha Vinculada ✅
                                </span>
                            )}
                        </div>

                        <div className="bg-secondary-500 bg-opacity-10 border-l-4 border-secondary-700 p-6 rounded-lg mb-8">
                            <h3 className="font-semibold text-neutral-900 mb-3">ℹ️ Informações Importantes</h3>
                            <ul className="space-y-2 text-neutral-700">
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Anonimato garantido:</strong> Suas respostas são confidenciais e protegidas por LGPD</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Tempo estimado:</strong> 15-20 minutos</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Total de perguntas:</strong> Responda com sinceridade usando escala de 1 a 5</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Finalidade:</strong> Avaliar clima organizacional e identificar oportunidades de melhoria</span>
                                </li>
                            </ul>
                        </div>

                        <button
                            onClick={() => setStep('validate')}
                            className="btn-primary w-full"
                        >
                            Começar Diagnóstico
                        </button>
                    </div>
                )}

                {/* Validation Step */}
                {step === 'validate' && (
                    <div className="card-premium animate-fade-in">
                        <h2 className="text-2xl font-bold text-neutral-900 mb-6">
                            Identificação
                        </h2>

                        {error && (
                            <div className="alert-danger mb-6 flex items-start">
                                <AlertCircle className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                        )}

                        <form onSubmit={handleValidation} className="space-y-6">
                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <User className="inline h-4 w-4 mr-2" />
                                    CPF
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    placeholder="000.000.000-00"
                                    value={formData.cpf}
                                    onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
                                    required
                                    maxLength={14}
                                />
                                <p className="text-xs text-neutral-500 mt-1">
                                    Usado apenas para evitar duplicidade. Não será armazenado em texto puro.
                                </p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <Mail className="inline h-4 w-4 mr-2" />
                                    E-mail
                                </label>
                                <input
                                    type="email"
                                    className="input"
                                    placeholder="seu@email.com"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <Building2 className="inline h-4 w-4 mr-2" />
                                    CNPJ da Empresa
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

                            <div>
                                <label className="block text-sm font-medium text-neutral-700 mb-2">
                                    <Hash className="inline h-4 w-4 mr-2" />
                                    Departamento/Setor (Opcional)
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    placeholder="Ex: RH, TI, Vendas..."
                                    value={formData.department_name}
                                    onChange={(e) => setFormData({ ...formData, department_name: e.target.value })}
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="btn-primary w-full flex items-center justify-center"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="animate-spin h-5 w-5 mr-2" />
                                        Validando...
                                    </>
                                ) : (
                                    'Próximo'
                                )}
                            </button>
                        </form>
                    </div>
                )}

                {/* Consent Step */}
                {step === 'consent' && (
                    <div className="card-premium animate-fade-in">
                        <h2 className="text-2xl font-bold text-neutral-900 mb-6">
                            Termo de Consentimento LGPD
                        </h2>

                        {validationResult && (
                            <div className="bg-primary-900 bg-opacity-5 border border-primary-900 border-opacity-20 p-4 rounded-lg mb-6">
                                <p className="text-neutral-900 font-medium">
                                    Organização: {validationResult.organization_name}
                                </p>
                            </div>
                        )}

                        {error && (
                            <div className="alert-danger mb-6">
                                {error}
                            </div>
                        )}

                        <div className="bg-neutral-100 p-6 rounded-lg mb-6 max-h-96 overflow-y-auto text-legal">
                            <h3 className="font-semibold text-neutral-900 mb-4">Termo de Consentimento para Tratamento de Dados Pessoais</h3>

                            <p className="mb-4">
                                Ao aceitar este termo, você autoriza o tratamento de seus dados pessoais pelo sistema SIMDCCO,
                                em conformidade com a Lei Geral de Proteção de Dados (LGPD - Lei 13.709/2018).
                            </p>

                            <h4 className="font-semibold text-neutral-900 mb-2">1. Finalidade do Tratamento</h4>
                            <p className="mb-4">
                                Seus dados serão utilizados exclusivamente para: (a) Realização de diagnóstico organizacional;
                                (b) Avaliação de clima e cultura organizacional; (c) Identificação de riscos psicossociais conforme NR-01;
                                (d) Geração de relatórios técnicos agregados.
                            </p>

                            <h4 className="font-semibold text-neutral-900 mb-2">2. Dados Coletados e Proteção</h4>
                            <p className="mb-4">
                                Coletamos: CPF, e-mail e CNPJ (hasheados via SHA-256 antes do armazenamento), respostas ao questionário,
                                departamento e metadados de sessão. Garantimos criptografia em repouso e em trânsito.
                            </p>

                            <h4 className="font-semibold text-neutral-900 mb-2">3. Direitos do Titular</h4>
                            <p className="mb-4">
                                Você pode: (a) Solicitar exclusão dos seus dados; (b) Revogar consentimento;
                                (c) Solicitar cópia dos dados armazenados.
                            </p>

                            <h4 className="font-semibold text-neutral-900 mb-2">4. Compartilhamento</h4>
                            <p className="mb-4">
                                Dados individualizados não serão compartilhados. Apenas relatórios agregados e anônimos
                                serão disponibilizados à sua organização.
                            </p>

                            <p className="mt-6 text-xs text-neutral-500">
                                Versão do termo: 1.0 | Data: 24/01/2026
                            </p>
                        </div>

                        <div className="flex items-start mb-6">
                            <input
                                type="checkbox"
                                id="consent"
                                checked={consentAccepted}
                                onChange={(e) => setConsentAccepted(e.target.checked)}
                                className="mt-1 h-5 w-5 text-primary-900 rounded border-neutral-300 focus:ring-primary-500"
                            />
                            <label htmlFor="consent" className="ml-3 text-neutral-700">
                                Li e aceito os termos acima. Autorizo o tratamento dos meus dados pessoais conforme descrito.
                            </label>
                        </div>

                        <button
                            onClick={handleConsent}
                            disabled={!consentAccepted || loading}
                            className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="animate-spin h-5 w-5 mr-2" />
                                    Processando...
                                </>
                            ) : (
                                'Aceitar e Continuar'
                            )}
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default function RespondentWelcome() {
    return (
        <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="h-12 w-12 animate-spin text-primary-900" /></div>}>
            <RespondentContent />
        </Suspense>
    )
}
