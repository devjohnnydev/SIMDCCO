"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Shield, Loader2, CheckCircle, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiService } from '@/lib/api'

interface Question {
    id: number
    type: string
    vector: string | null
    dimension: string | null
    text: string
    order: number
}

export default function Questionnaire() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [questions, setQuestions] = useState<Question[]>([])
    const [currentIndex, setCurrentIndex] = useState(0)
    const [answers, setAnswers] = useState<Record<number, number>>({})
    const [sessionData, setSessionData] = useState<any>(null)
    const [error, setError] = useState('')

    useEffect(() => {
        // Check session
        const session = sessionStorage.getItem('respondent_session')
        if (!session) {
            router.push('/respondent')
            return
        }

        setSessionData(JSON.parse(session))
        loadQuestions()
    }, [])

    const loadQuestions = async () => {
        try {
            const response = await apiService.getAllQuestions()
            setQuestions(response.data)
        } catch (err) {
            setError('Erro ao carregar questionário.')
        } finally {
            setLoading(false)
        }
    }

    const handleAnswer = (value: number) => {
        const currentQuestion = questions[currentIndex]
        setAnswers(prev => ({ ...prev, [currentQuestion.id]: value }))
    }

    const handleNext = () => {
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(currentIndex + 1)
        }
    }

    const handlePrevious = () => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1)
        }
    }

    const handleSubmit = async () => {
        // Validate all answered
        if (Object.keys(answers).length !== questions.length) {
            setError(`Por favor, responda todas as ${questions.length} perguntas antes de enviar.`)
            return
        }

        setSubmitting(true)
        setError('')

        try {
            // Convert answers to string keys as API expects
            const answersForApi: Record<string, number> = {}
            Object.entries(answers).forEach(([key, value]) => {
                answersForApi[key.toString()] = value
            })

            await apiService.submitResponse({
                cpf: sessionData.cpf,
                cnpj: sessionData.cnpj,
                department_id: sessionData.department_id,
                answers: answersForApi,
                session_id: sessionData.session_id,
                campaign_slug: sessionData.campaign_slug
            })

            // Clear session and redirect to completion
            sessionStorage.removeItem('respondent_session')
            router.push('/respondent/complete')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao enviar respostas. Tente novamente.')
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="h-12 w-12 animate-spin text-primary-900" />
            </div>
        )
    }

    if (!questions.length) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-neutral-600">Nenhuma pergunta disponível.</p>
            </div>
        )
    }

    const currentQuestion = questions[currentIndex]
    const progress = ((currentIndex + 1) / questions.length) * 100
    const answeredCount = Object.keys(answers).length
    const currentAnswer = answers[currentQuestion.id]

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-neutral-50">
            {/* Header with Progress */}
            <div className="bg-white border-b border-neutral-200 shadow-sm sticky top-0 z-50">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                            <Shield className="h-6 w-6 text-primary-900" />
                            <span className="text-xl font-bold text-primary-900">SIMDCCO</span>
                        </div>
                        <div className="text-sm text-neutral-600">
                            Pergunta {currentIndex + 1} de {questions.length}
                        </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${progress}%` }} />
                    </div>

                    <div className="flex justify-between mt-2 text-xs text-neutral-500">
                        <span>Progresso: {Math.round(progress)}%</span>
                        <span>Respondidas: {answeredCount}/{questions.length}</span>
                    </div>
                </div>
            </div>

            {/* Question Card */}
            <div className="container mx-auto px-6 py-12 max-w-3xl">
                <div className="card-premium animate-fade-in">
                    {/* Question Type Badge */}
                    <div className="flex items-center justify-between mb-6">
                        <span className={`px-4 py-2 rounded-full text-sm font-medium ${currentQuestion.type === 'imco'
                            ? 'bg-primary-900 bg-opacity-10 text-primary-900'
                            : 'bg-secondary-700 bg-opacity-10 text-secondary-700'
                            }`}>
                            {currentQuestion.type === 'imco' ? 'IMCO - Clima Organizacional' : 'FDAC - Cultura Organizacional'}
                        </span>
                        {currentQuestion.vector && (
                            <span className="text-sm text-neutral-500">
                                {currentQuestion.vector}
                            </span>
                        )}
                    </div>

                    {/* Question Text */}
                    <h2 className="text-2xl font-bold text-neutral-900 mb-8 leading-relaxed">
                        {currentQuestion.text}
                    </h2>

                    {/* Likert Scale */}
                    <div className="mb-8">
                        <div className="flex justify-between mb-3 text-sm text-neutral-600">
                            <span>Discordo Totalmente</span>
                            <span>Concordo Totalmente</span>
                        </div>

                        <div className="grid grid-cols-5 gap-4">
                            {[1, 2, 3, 4, 5].map((value) => (
                                <button
                                    key={value}
                                    onClick={() => handleAnswer(value)}
                                    className={`
                    py-6 rounded-xl border-2 transition-all duration-200
                    hover:scale-105 active:scale-95
                    ${currentAnswer === value
                                            ? 'bg-primary-900 border-primary-900 text-white shadow-lg'
                                            : 'bg-white border-neutral-300 text-neutral-700 hover:border-primary-500'
                                        }
                  `}
                                >
                                    <div className="text-3xl font-bold">{value}</div>
                                </button>
                            ))}
                        </div>

                        <div className="flex justify-between mt-2 text-xs text-neutral-500">
                            {['1', '2', '3', '4', '5'].map(v => (
                                <span key={v} className="w-16 text-center">{v}</span>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="alert-danger mb-6">
                            {error}
                        </div>
                    )}

                    {/* Navigation */}
                    <div className="flex items-center justify-between pt-6 border-t border-neutral-200">
                        <button
                            onClick={handlePrevious}
                            disabled={currentIndex === 0}
                            className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                        >
                            <ChevronLeft className="h-5 w-5 mr-1" />
                            Anterior
                        </button>

                        {currentIndex === questions.length - 1 ? (
                            <button
                                onClick={handleSubmit}
                                disabled={!currentAnswer || submitting}
                                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                            >
                                {submitting ? (
                                    <>
                                        <Loader2 className="animate-spin h-5 w-5 mr-2" />
                                        Enviando...
                                    </>
                                ) : (
                                    <>
                                        Enviar Respostas
                                        <CheckCircle className="h-5 w-5 ml-2" />
                                    </>
                                )}
                            </button>
                        ) : (
                            <button
                                onClick={handleNext}
                                disabled={!currentAnswer}
                                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                            >
                                Próxima
                                <ChevronRight className="h-5 w-5 ml-1" />
                            </button>
                        )}
                    </div>
                </div>

                {/* Helper Text */}
                <p className="text-center text-sm text-neutral-500 mt-6">
                    💡 Suas respostas são anônimas e criptografadas. Responda com sinceridade.
                </p>
            </div>
        </div>
    )
}
