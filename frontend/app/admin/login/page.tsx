"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, Loader2, AlertCircle, LogIn } from 'lucide-react'
import { apiService } from '@/lib/api'

export default function AdminLogin() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [credentials, setCredentials] = useState({
        email: '',
        password: ''
    })

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            const response = await apiService.login(credentials.email, credentials.password)

            // Store tokens
            localStorage.setItem('access_token', response.data.access_token)
            localStorage.setItem('refresh_token', response.data.refresh_token)

            // Redirect to dashboard
            router.push('/admin/dashboard')
        } catch (err: any) {
            console.error('Login error:', err)
            let errorMessage = 'Credenciais inválidas. Verifique e tente novamente.'

            if (err.response?.data?.detail) {
                const detail = err.response.data.detail
                if (typeof detail === 'string') {
                    errorMessage = detail
                } else if (Array.isArray(detail)) {
                    // Handle Pydantic validation errors
                    errorMessage = detail.map((e: any) => e.msg).join(', ')
                } else if (typeof detail === 'object') {
                    errorMessage = JSON.stringify(detail)
                }
            }

            setError(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-700 to-primary-900 flex items-center justify-center px-6">
            <div className="max-w-md w-full">
                {/* Logo */}
                <Link href="/" className="flex items-center justify-center space-x-2 mb-8">
                    <Shield className="h-12 w-12 text-white" />
                    <span className="text-3xl font-bold text-white">SIMDCCO</span>
                </Link>

                {/* Login Card */}
                <div className="bg-white rounded-2xl shadow-2xl p-8">
                    <div className="text-center mb-8">
                        <h1 className="text-2xl font-bold text-neutral-900 mb-2">
                            Painel Administrativo
                        </h1>
                        <p className="text-neutral-600">
                            Acesso restrito para administradores
                        </p>
                    </div>

                    {error && (
                        <div className="alert-danger mb-6 flex items-start">
                            <AlertCircle className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" />
                            <span>{error}</span>
                        </div>
                    )}

                    <form onSubmit={handleLogin} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-neutral-700 mb-2">
                                E-mail
                            </label>
                            <input
                                type="email"
                                className="input"
                                placeholder="admin@simdcco.com"
                                value={credentials.email}
                                onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                                required
                                autoComplete="email"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-neutral-700 mb-2">
                                Senha
                            </label>
                            <input
                                type="password"
                                className="input"
                                placeholder="••••••••"
                                value={credentials.password}
                                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                                required
                                autoComplete="current-password"
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
                                    Entrando...
                                </>
                            ) : (
                                <>
                                    <LogIn className="h-5 w-5 mr-2" />
                                    Entrar
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-sm text-neutral-500">
                            Credenciais padrão (desenvolvimento):
                            <br />
                            <code className="text-xs bg-neutral-100 px-2 py-1 rounded mt-1 inline-block">
                                admin@simdcco.com / admin123
                            </code>
                        </p>
                        <p className="text-xs text-danger-700 mt-2">
                            ⚠️ Altere a senha em produção!
                        </p>
                    </div>
                </div>

                <div className="text-center mt-6">
                    <Link href="/" className="text-white text-sm hover:text-primary-100 transition">
                        ← Voltar ao Início
                    </Link>
                </div>
            </div>
        </div>
    )
}
