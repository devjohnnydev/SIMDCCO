"use client"

import Link from 'next/link'
import { Shield, FileCheck, Users, BarChart3, ArrowRight, CheckCircle } from 'lucide-react'

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100">
            {/* Header/Navbar */}
            <nav className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                            <Shield className="h-8 w-8 text-primary-900" />
                            <span className="text-2xl font-bold text-primary-900">SIMDCCO</span>
                        </div>
                        <div className="flex items-center space-x-6">
                            <Link href="/legal" className="text-neutral-700 hover:text-primary-900 transition">
                                Compliance
                            </Link>
                            <Link href="/respondent" className="btn-primary" style={{ display: 'none' }}>
                                Responder Questionário
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="container mx-auto px-6 py-20">
                <div className="grid md:grid-cols-2 gap-12 items-center">
                    <div className="animate-fade-in">
                        <div className="inline-block bg-primary-900 bg-opacity-10 text-primary-900 px-4 py-2 rounded-full text-sm font-medium mb-6">
                            ⚖️ Idealizado por Perito Judicial
                        </div>
                        <h1 className="text-5xl font-bold text-neutral-900 mb-6 leading-tight">
                            Proteja sua Empresa com <span className="text-primary-900">Conformidade NR-01</span>
                        </h1>
                        <p className="text-xl text-neutral-600 mb-8 leading-relaxed">
                            Sistema de Diagnóstico de Saúde Mental, Clima e Cultura Organizacional.
                            Gere <strong>evidências documentais juridicamente defensáveis</strong> e
                            evite riscos trabalhistas.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4">
                            <Link href="/demo" className="btn-primary flex items-center justify-center">
                                Solicitar Demonstração
                                <ArrowRight className="ml-2 h-5 w-5" />
                            </Link>
                        </div>
                    </div>

                    <div className="hidden md:block">
                        <div className="card-premium hover-lift">
                            <div className="flex items-center justify-between mb-4">
                                <FileCheck className="h-12 w-12 text-primary-900" />
                                <span className="badge-low">Conformidade Ativa</span>
                            </div>
                            <h3 className="text-2xl font-bold text-neutral-900 mb-2">
                                Evidência Técnica NR-01
                            </h3>
                            <p className="text-neutral-600 mb-6">
                                Laudos e relatórios com valor probatório para auditorias e processos judiciais
                            </p>
                            <div className="border-t border-neutral-200 pt-4 flex items-center justify-between">
                                <span className="text-sm text-neutral-500">Relatório: SIMDCCO-2026-00001</span>
                                <CheckCircle className="h-5 w-5 text-secondary-700" />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Problem Section */}
            <section className="bg-danger-700 bg-opacity-5 border-y border-danger-700 border-opacity-20 py-16">
                <div className="container mx-auto px-6">
                    <div className="text-center max-w-3xl mx-auto">
                        <h2 className="text-3xl font-bold text-neutral-900 mb-4">
                            ⚠️ Riscos Jurídicos da Falta de Conformidade
                        </h2>
                        <p className="text-lg text-neutral-700 mb-8">
                            Empresas que não avaliam riscos psicossociais enfrentam:
                        </p>
                        <div className="grid md:grid-cols-4 gap-6">
                            {[
                                { label: 'Multas Trabalhistas', icon: '💰' },
                                { label: 'Ações Judiciais', icon: '⚖️' },
                                { label: 'Afastamentos INSS', icon: '🏥' },
                                { label: 'Dano Reputacional', icon: '📉' }
                            ].map((item, idx) => (
                                <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
                                    <div className="text-4xl mb-3">{item.icon}</div>
                                    <div className="font-semibold text-neutral-900">{item.label}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* Solution Section */}
            <section className="container mx-auto px-6 py-20">
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold text-neutral-900 mb-4">
                        Como o SIMDCCO Protege sua Empresa
                    </h2>
                    <p className="text-xl text-neutral-600 max-w-2xl mx-auto">
                        Ferramenta completa de diagnóstico, compliance e defesa jurídica
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {[
                        {
                            icon: Users,
                            title: 'Diagnóstico Estruturado',
                            description: '100 perguntas validadas (IMCO + FDAC) para mapear clima e cultura organizacional com precisão técnica.'
                        },
                        {
                            icon: BarChart3,
                            title: 'Análise de Riscos',
                            description: 'Dashboards executivos e relatórios departamentais identificando riscos psicossociais por NR-01.'
                        },
                        {
                            icon: FileCheck,
                            title: 'Prova Documental',
                            description: 'Laudos numerados e versionados com fundamentação legal para uso em auditorias e processos.'
                        }
                    ].map((feature, idx) => (
                        <div key={idx} className="card hover-lift text-center">
                            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-900 bg-opacity-10 rounded-full mb-6">
                                <feature.icon className="h-8 w-8 text-primary-900" />
                            </div>
                            <h3 className="text-xl font-bold text-neutral-900 mb-3">{feature.title}</h3>
                            <p className="text-neutral-600">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section className="bg-primary-900 text-white py-16">
                <div className="container mx-auto px-6 text-center">
                    <h2 className="text-3xl font-bold mb-4">
                        Garanta a Conformidade da sua Empresa Agora
                    </h2>
                    <p className="text-xl mb-8 text-primary-100">
                        Evite passivos trabalhistas e demonstre conformidade com a NR-01
                    </p>
                    <Link href="/demo" className="inline-block bg-white text-primary-900 px-8 py-4 rounded-lg font-bold text-lg hover:bg-neutral-100 transition active:scale-95">
                        Solicitar Demonstração Gratuita
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-neutral-900 text-neutral-300 py-12">
                <div className="container mx-auto px-6">
                    <div className="grid md:grid-cols-3 gap-8">
                        <div>
                            <div className="flex items-center space-x-2 mb-4">
                                <Shield className="h-6 w-6 text-primary-500" />
                                <span className="text-xl font-bold text-white">SIMDCCO</span>
                            </div>
                            <p className="text-sm">
                                Sistema de Proteção Jurídica Preventiva para Saúde Mental Organizacional
                            </p>
                        </div>
                        <div>
                            <h4 className="text-white font-semibold mb-4">Legal</h4>
                            <ul className="space-y-2 text-sm">
                                <li><Link href="/legal" className="hover:text-white transition">Compliance LGPD</Link></li>
                                <li><Link href="/legal" className="hover:text-white transition">Base Legal NR-01</Link></li>
                                <li><Link href="/legal" className="hover:text-white transition">Metodologia IMCO/FDAC</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="text-white font-semibold mb-4">Contato</h4>
                            <ul className="space-y-2 text-sm">
                                <li>contato@simdcco.com.br</li>
                                <li>(11) 9999-9999</li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-neutral-700 mt-12 pt-6 flex justify-between items-center text-sm">
                        <div className="text-center flex-1">
                            © 2026 SIMDCCO. Todos os direitos reservados.
                        </div>
                        <Link
                            href="/admin/login"
                            className="text-neutral-500 hover:text-neutral-200 transition text-sm opacity-70 hover:opacity-100"
                        >
                            • login
                        </Link>
                    </div>
                </div>
            </footer>
        </div>
    )
}
