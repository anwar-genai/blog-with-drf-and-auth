'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import PostCard from '@/components/PostCard';
import ComposePost from '@/components/ComposePost';
import api from '@/lib/api';

export default function Home() {
  const { isAuthenticated } = useAuth();
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await api.getPosts();
      setPosts(response.results || []);
    } catch (err) {
      setError('Failed to load posts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="sticky top-0 bg-white/80 backdrop-blur-md border-b border-gray-200 p-4">
        <h1 className="text-xl font-bold">Home</h1>
      </div>

      {/* Compose - Only show when authenticated */}
      <ComposePost onPostCreated={fetchPosts} />

      {/* Login prompt for guests */}
      {!isAuthenticated && (
        <div className="bg-blue-50 border-b border-blue-100 p-4">
          <div className="text-center">
            <p className="text-gray-700 mb-3">
              Join the conversation! Sign in to create posts, like, and comment.
            </p>
            <Link
              href="/login"
              className="inline-block bg-blue-500 text-white font-semibold px-6 py-2 rounded-full hover:bg-blue-600 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      )}

      {/* Feed */}
      <div>
        {loading ? (
          <div className="p-8 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="p-8 text-center text-red-500">{error}</div>
        ) : posts.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No posts yet</div>
        ) : (
          posts.map((post) => (
            <PostCard key={post.id} post={post} onUpdate={fetchPosts} />
          ))
        )}
      </div>
    </div>
  );
}