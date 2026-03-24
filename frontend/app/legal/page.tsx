"use client"

import Link from 'next/link'
import { Shield, Scale, FileText, CheckCircle, AlertTriangle, Book } from 'lucide-react'

export default function LegalPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100">
            {/* Header */}
            <nav className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-2">
                            <Shield className="h-8 w-8 text-primary-900" />
                            <span className="text-2xl font-bold text-primary-900">SIMDCCO</span>
                        </Link>
                        <Link href="/" className="text-neutral-700 hover:text-primary-900 transition">
                            Voltar ao início
                        </Link>
                    </div>
                </div>
            </nav>

            <div className="container mx-auto px-6 py-16 max-w-5xl">
                {/* Hero */}
                <div className="text-center mb-16">
                    <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-900 bg-opacity-10 rounded-full mb-6">
                        <Scale className="h-10 w-10 text-primary-900" />
                    </div>
                    <h1 className="text-4xl font-bold text-neutral-900 mb-4">
                        Conformidade Legal e Compliance
                    </h1>
                    <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
                        O SIMDCCO foi desenvolvido para garantir total conformidade com a legislação brasileira
                        de saúde mental no trabalho e proteção de dados.
                    </p>
                </div>

                {/* NR-01 Section */}
                <div className="card mb-8">
                    <div className="flex items-start space-x-4 mb-6">
                        <div className="p-3 bg-primary-900 bg-opacity-10 rounded-lg">
                            <FileText className="h-6 w-6 text-primary-900" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-neutral-900 mb-2">
                                NR-01 - Gerenciamento de Riscos Ocupacionais
                            </h2>
                            <p className="text-neutral-600">
                                Base legal do sistema de diagnóstico de saúde mental
                            </p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-neutral-50 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-3">O que a NR-01 exige?</h3>
                            <ul className="space-y-2 text-neutral-700">
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span>Identificação de perigos e avaliação de riscos ocupacionais, incluindo <strong>riscos psicossociais</strong></span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span>Implementação de medidas de prevenção e controle</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span>Manutenção de <strong>documentação e registros</strong> das avaliações</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span>Capacidade de <strong>comprovar</strong> as ações preventivas em auditorias e fiscalizações</span>
                                </li>
                            </ul>
                        </div>

                        <div className="bg-primary-900 bg-opacity-5 p-6 rounded-lg border border-primary-900 border-opacity-20">
                            <h3 className="font-semibold text-neutral-900 mb-3 flex items-center">
                                <AlertTriangle className="h-5 w-5 text-warning-500 mr-2" />
                                Como o SIMDCCO atende à NR-01
                            </h3>
                            <ul className="space-y-2 text-neutral-700">
                                <li className="flex items-start">
                                    <span className="text-primary-900 font-bold mr-2">✓</span>
                                    <span>Avalia sistematicamente fatores de risco psicossocial através de questionários validados (IMCO + FDAC)</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="text-primary-900 font-bold mr-2">✓</span>
                                    <span>Gera relatórios técnicos numerados com fundamentação legal</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="text-primary-900 font-bold mr-2">✓</span>
                                    <span>Mantém histórico imutável de avaliações e evidências documentais</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="text-primary-900 font-bold mr-2">✓</span>
                                    <span>Produz laudos com <strong>valor probatório</strong> para uso em auditorias e processos judiciais</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* LGPD Section */}
                <div className="card mb-8">
                    <div className="flex items-start space-x-4 mb-6">
                        <div className="p-3 bg-secondary-700 bg-opacity-10 rounded-lg">
                            <Shield className="h-6 w-6 text-secondary-700" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-neutral-900 mb-2">
                                LGPD - Lei Geral de Proteção de Dados
                            </h2>
                            <p className="text-neutral-600">
                                Proteção máxima de dados sensíveis dos respondentes
                            </p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-neutral-50 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-3">Medidas de Segurança Implementadas</h3>
                            <ul className="grid md:grid-cols-2 gap-4 text-neutral-700">
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Hash SHA-256</strong> para CPF, CNPJ e e-mail</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Anonimização</strong> de respostas</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Registro de consentimento</strong> com timestamp e IP</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Direito ao esquecimento</strong> implementado</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Logs de auditoria</strong> imutáveis</span>
                                </li>
                                <li className="flex items-start">
                                    <CheckCircle className="h-5 w-5 text-secondary-700 mr-2 mt-0.5 flex-shrink-0" />
                                    <span><strong>Termos de uso</strong> e política de privacidade</span>
                                </li>
                            </ul>
                        </div>

                        <div className="bg-secondary-700 bg-opacity-5 p-6 rounded-lg border border-secondary-700 border-opacity-20">
                            <h3 className="font-semibold text-neutral-900 mb-2">Dados Coletados</h3>
                            <p className="text-sm text-neutral-600 mb-3">
                                Para fins de diagnóstico organizacional e em conformidade com a NR-01:
                            </p>
                            <ul className="grid md:grid-cols-2 gap-2 text-sm text-neutral-700">
                                <li>• CPF (hash)</li>
                                <li>• E-mail (hash)</li>
                                <li>• CNPJ da organização (hash)</li>
                                <li>• Departamento (não identificável)</li>
                                <li>• Respostas do questionário (anônimas)</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Methodology Section */}
                <div className="card mb-8">
                    <div className="flex items-start space-x-4 mb-6">
                        <div className="p-3 bg-primary-900 bg-opacity-10 rounded-lg">
                            <Book className="h-6 w-6 text-primary-900" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-neutral-900 mb-2">
                                Metodologia Científica
                            </h2>
                            <p className="text-neutral-600">
                                Instrumentos validados academicamente
                            </p>
                        </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="bg-neutral-50 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-2">IMCO</h3>
                            <p className="text-sm text-neutral-600 mb-3">Inventário de Medição de Clima Organizacional</p>
                            <ul className="text-sm text-neutral-700 space-y-1">
                                <li>• <strong>88 questões</strong></li>
                                <li>• 11 vetores de clima</li>
                                <li>• 5 dimensões organizacionais</li>
                                <li>• Instrumento validado cientificamente</li>
                            </ul>
                        </div>

                        <div className="bg-neutral-50 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-2">FDAC</h3>
                            <p className="text-sm text-neutral-600 mb-3">Funções Dinâmicas de Análise Cultural</p>
                            <ul className="text-sm text-neutral-700 space-y-1">
                                <li>• <strong>12 questões</strong></li>
                                <li>• Análise de cultura organizacional</li>
                                <li>• Complementar ao IMCO</li>
                                <li>• Base para recomendações</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* CTA */}
                <div className="text-center bg-primary-900 text-white p-12 rounded-2xl">
                    <h2 className="text-3xl font-bold mb-4">
                        Pronto para Garantir Conformidade?
                    </h2>
                    <p className="text-primary-100 mb-8 text-lg">
                        Inicie seu diagnóstico de saúde mental organizacional agora
                    </p>
                    <Link href="/demo" className="inline-block bg-primary-700 text-white px-8 py-4 rounded-lg font-bold hover:bg-primary-600 transition">
                        Solicitar Demonstração
                    </Link>
                </div>
            </div>

            {/* Footer */}
            <footer className="bg-neutral-900 text-neutral-300 py-8 mt-16">
                <div className="container mx-auto px-6 text-center">
                    <p className="text-sm">© 2026 SIMDCCO. Sistema de Proteção Jurídica Preventiva para Saúde Mental Organizacional</p>
                </div>
            </footer>
        </div>
    )
}
