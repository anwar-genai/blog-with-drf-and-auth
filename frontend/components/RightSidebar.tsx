'use client';

import { Search } from 'lucide-react';

export default function RightSidebar() {
  const trends = [
    { category: 'Technology', title: '#NextJS', posts: '12.3K' },
    { category: 'Programming', title: '#Django', posts: '8.5K' },
    { category: 'Web Development', title: '#TailwindCSS', posts: '25.1K' },
  ];

  const suggestions = [
    { username: 'john_doe', handle: '@johndoe', avatar: null },
    { username: 'jane_smith', handle: '@janesmith', avatar: null },
    { username: 'tech_guru', handle: '@techguru', avatar: null },
  ];

  return (
    <aside className="w-80 flex-shrink-0 hidden lg:block" suppressHydrationWarning>
      <div className="sticky top-0 p-4 space-y-4" suppressHydrationWarning>
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search"
            className="w-full pl-12 pr-4 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors"
            suppressHydrationWarning
          />
        </div>

        {/* Trends */}
        <div className="bg-gray-50 rounded-2xl p-4">
          <h2 className="text-xl font-bold mb-3">Trends for you</h2>
          <div className="space-y-3">
            {trends.map((trend, index) => (
              <div key={index} className="hover:bg-gray-100 -mx-2 px-2 py-2 rounded cursor-pointer transition-colors">
                <p className="text-sm text-gray-500">{trend.category} · Trending</p>
                <p className="font-bold">{trend.title}</p>
                <p className="text-sm text-gray-500">{trend.posts} posts</p>
              </div>
            ))}
          </div>
          <button className="text-blue-500 hover:underline mt-3" suppressHydrationWarning>Show more</button>
        </div>

        {/* Who to follow */}
        <div className="bg-gray-50 rounded-2xl p-4" suppressHydrationWarning>
          <h2 className="text-xl font-bold mb-3">Who to follow</h2>
          <div className="space-y-3">
            {suggestions.map((user, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-300"></div>
                  <div>
                    <p className="font-semibold">{user.username}</p>
                    <p className="text-sm text-gray-500">{user.handle}</p>
                  </div>
                </div>
                <button className="px-4 py-1.5 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-colors" suppressHydrationWarning>
                  Follow
                </button>
              </div>
            ))}
          </div>
          <button className="text-blue-500 hover:underline mt-3" suppressHydrationWarning>Show more</button>
        </div>

        {/* Footer Links */}
        <div className="text-sm text-gray-500 space-y-2">
          <div className="flex flex-wrap gap-2">
            <a href="#" className="hover:underline">Terms of Service</a>
            <a href="#" className="hover:underline">Privacy Policy</a>
            <a href="#" className="hover:underline">Cookie Policy</a>
          </div>
          <p>© 2024 Blog Platform</p>
        </div>
      </div>
    </aside>
  );
}
