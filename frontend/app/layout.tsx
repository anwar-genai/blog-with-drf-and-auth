import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/contexts/AuthContext'
import Sidebar from '@/components/Sidebar'
import RightSidebar from '@/components/RightSidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Blog Platform',
  description: 'A modern blogging platform built with Next.js and Django',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-white">
            <div className="max-w-7xl mx-auto flex">
              {/* Left Sidebar */}
              <Sidebar />

              {/* Main Content */}
              <main className="flex-1 min-w-0 border-x border-gray-200">
                {children}
              </main>

              {/* Right Sidebar */}
              <RightSidebar />
            </div>
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}