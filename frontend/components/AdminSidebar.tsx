"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Shield, LayoutDashboard, Building2, Users, Calendar, FileText, LogOut } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function AdminSidebar() {
    const pathname = usePathname()
    const router = useRouter()

    const menuItems = [
        { href: '/admin/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
        { href: '/admin/organizations', icon: Building2, label: 'Empresas' },
        { href: '/admin/leads', icon: Users, label: 'Leads' },
        { href: '/admin/campaigns', icon: Calendar, label: 'Campanhas' },
    ]

    const handleLogout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/admin/login')
    }

    return (
        <div className="h-screen w-64 bg-white border-r border-neutral-200 flex flex-col fixed left-0 top-0">
            {/* Logo */}
            <Link href="/admin/dashboard" className="flex items-center space-x-2 p-6 border-b border-neutral-200">
                <Shield className="h-8 w-8 text-primary-900" />
                <div>
                    <span className="text-xl font-bold text-primary-900 block">SIMDCCO</span>
                    <span className="text-xs text-neutral-500">Admin Panel</span>
                </div>
            </Link>

            {/* Menu Items */}
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
                {menuItems.map((item) => {
                    const isActive = pathname === item.href || pathname.startsWith(item.href + '/')
                    const Icon = item.icon

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${isActive
                                    ? 'bg-primary-900 text-white'
                                    : 'text-neutral-700 hover:bg-neutral-100'
                                }`}
                        >
                            <Icon className="h-5 w-5" />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    )
                })}
            </nav>

            {/* Logout */}
            <div className="p-4 border-t border-neutral-200">
                <button
                    onClick={handleLogout}
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-neutral-700 hover:bg-red-50 hover:text-red-700 transition w-full"
                >
                    <LogOut className="h-5 w-5" />
                    <span className="font-medium">Sair</span>
                </button>
            </div>
        </div>
    )
}
