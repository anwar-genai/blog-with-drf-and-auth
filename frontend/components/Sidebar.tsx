'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Home, 
  Search, 
  Bell, 
  Mail, 
  Bookmark, 
  User, 
  MoreHorizontal,
  LogOut,
  LogIn
} from 'lucide-react';

const navigation = [
  { name: 'Home', href: '/', icon: Home },
  { name: 'Explore', href: '/explore', icon: Search },
  { name: 'Notifications', href: '/notifications', icon: Bell },
  { name: 'Messages', href: '/messages', icon: Mail },
  { name: 'Bookmarks', href: '/bookmarks', icon: Bookmark },
  { name: 'Profile', href: '/profile', icon: User },
  { name: 'More', href: '#', icon: MoreHorizontal },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <aside className="w-64 xl:w-72 flex-shrink-0">
      <div className="sticky top-0 h-screen flex flex-col p-4">
        {/* Logo */}
        <Link href="/" className="mb-8">
          <h1 className="text-2xl font-bold text-blue-500">Blog</h1>
        </Link>

        {/* Navigation */}
        <nav className="flex-1">
          <ul className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={`
                      flex items-center gap-4 px-4 py-3 rounded-full
                      transition-colors duration-200
                      ${isActive 
                        ? 'font-bold text-black' 
                        : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Icon className={`w-6 h-6 ${isActive ? 'stroke-2' : ''}`} />
                    <span className="text-xl hidden xl:block">{item.name}</span>
                  </Link>
                </li>
              );
            })}

            {/* Auth Links */}
            {!isAuthenticated && (
              <li>
                <Link
                  href="/login"
                  className="flex items-center gap-4 px-4 py-3 rounded-full text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                >
                  <LogIn className="w-6 h-6" />
                  <span className="text-xl hidden xl:block">Login</span>
                </Link>
              </li>
            )}

            {isAuthenticated && (
              <li>
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-4 px-4 py-3 rounded-full text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                >
                  <LogOut className="w-6 h-6" />
                  <span className="text-xl hidden xl:block">Logout</span>
                </button>
              </li>
            )}
          </ul>
        </nav>

        {/* Post Button - Only show when authenticated */}
        {isAuthenticated && (
          <button className="w-full bg-blue-500 text-white font-bold py-3 px-8 rounded-full hover:bg-blue-600 transition-colors duration-200 mb-4">
            <span className="hidden xl:block">Post</span>
            <span className="xl:hidden">+</span>
          </button>
        )}

        {/* User Menu - Only show when authenticated */}
        {isAuthenticated && user && user.username && (
          <div className="p-3 rounded-full hover:bg-gray-100 cursor-pointer transition-colors duration-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                {user.username[0]?.toUpperCase() || 'U'}
              </div>
              <div className="hidden xl:block">
                <p className="font-semibold">{user.username}</p>
                <p className="text-sm text-gray-500">@{user.username}</p>
              </div>
              <MoreHorizontal className="w-5 h-5 ml-auto hidden xl:block" />
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
