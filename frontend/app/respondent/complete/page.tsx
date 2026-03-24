"use client"

import Link from 'next/link'
import { CheckCircle, Shield, Home } from 'lucide-react'

export default function QuestionnaireComplete() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-neutral-50 flex items-center justify-center px-6">
            <div className="max-w-2xl w-full">
                <div className="card-premium text-center animate-fade-in">
                    {/* Success Icon */}
                    <div className="inline-flex items-center justify-center w-24 h-24 bg-secondary-700 bg-opacity-10 rounded-full mb-8">
                        <CheckCircle className="h-12 w-12 text-secondary-700" />
                    </div>

                    {/* Title */}
                    <h1 className="text-3xl font-bold text-neutral-900 mb-4">
                        ✅ Questionário Enviado com Sucesso!
                    </h1>

                    {/* Thank you message */}
                    <p className="text-lg text-neutral-600 mb-8">
                        Agradecemos sua participação neste diagnóstico organizacional.
                        Suas respostas são extremamente valiosas para melhorar o ambiente de trabalho.
                    </p>

                    {/* Info Cards */}
                    <div className="grid md:grid-cols-2 gap-6 mb-8 text-left">
                        <div className="bg-primary-900 bg-opacity-5 border border-primary-900 border-opacity-20 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-2">🔒 Confidencialidade</h3>
                            <p className="text-sm text-neutral-600">
                                Suas respostas foram criptografadas e armazenadas de forma anônima,
                                seguindo rigorosamente a LGPD.
                            </p>
                        </div>

                        <div className="bg-secondary-700 bg-opacity-5 border border-secondary-700 border-opacity-20 p-6 rounded-lg">
                            <h3 className="font-semibold text-neutral-900 mb-2">📊 Próximos Passos</h3>
                            <p className="text-sm text-neutral-600">
                                Sua organização receberá relatórios agregados e anônimos com
                                análise técnica e recomendações.
                            </p>
                        </div>
                    </div>

                    {/* Additional Info */}
                    <div className="bg-neutral-100 p-6 rounded-lg mb-8 text-legal">
                        <h4 className="font-semibold text-neutral-900 mb-3">ℹ️ Informações Importantes</h4>
                        <ul className="space-y-2 text-left">
                            <li>• Você pode solicitar a exclusão dos seus dados a qualquer momento</li>
                            <li>• Não é possível editar as respostas após o envio</li>
                            <li>• Os resultados individuais não serão compartilhados com terceiros</li>
                            <li>• Para dúvidas sobre LGPD, entre em contato: privacidade@simdcco.com.br</li>
                        </ul>
                    </div>

                    {/* Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/" className="btn-primary flex items-center justify-center">
                            <Home className="h-5 w-5 mr-2" />
                            Voltar ao Início
                        </Link>
                        <Link href="/" className="btn-outline flex items-center justify-center">
                            <Shield className="h-5 w-5 mr-2" />
                            Sobre o SIMDCCO
                        </Link>
                    </div>

                    {/* Footer note */}
                    <p className="mt-8 text-xs text-neutral-500">
                        Sistema SIMDCCO - Diagnóstico de Saúde Mental e Clima Organizacional
                        <br />
                        Idealizado por Perito Judicial | Conformidade NR-01
                    </p>
                </div>
            </div>
        </div>
    )
}
