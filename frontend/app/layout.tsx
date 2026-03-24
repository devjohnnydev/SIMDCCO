import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'SIMDCCO - Sistema de Diagnóstico de Saúde Mental Organizacional',
    description: 'Sistema jurídico-tecnológico para compliance NR-01 e avaliação de riscos psicossociais. Idealizado por perito judicial.',
    keywords: ['NR-01', 'saúde mental', 'compliance', 'riscos psicossociais', 'IMCO', 'FDAC'],
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="pt-BR">
            <body className={inter.className}>{children}</body>
        </html>
    )
}
