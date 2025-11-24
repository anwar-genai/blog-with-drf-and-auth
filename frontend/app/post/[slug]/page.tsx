'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Heart, MessageCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import CommentSection from '@/components/CommentSection';
import api from '@/lib/api';

export default function PostDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [post, setPost] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);
  const [isLiking, setIsLiking] = useState(false);

  useEffect(() => {
    if (params.slug) {
      fetchPost();
    }
  }, [params.slug]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const data = await api.getPost(params.slug as string);
      setPost(data);
      setLiked(data.user_liked);
      setLikesCount(data.likes_count);
    } catch (error) {
      console.error('Failed to fetch post:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async () => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (isLiking) return;

    setIsLiking(true);
    try {
      const response = await api.likePost(post.id.toString());
      setLiked(response.liked);
      setLikesCount(response.likes_count);
    } catch (error) {
      console.error('Failed to like post:', error);
    } finally {
      setIsLiking(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="p-8 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="p-8 text-center">
        <p className="text-gray-500">Post not found</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="sticky top-0 bg-white/80 backdrop-blur-md border-b border-gray-200 p-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.back()}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-xl font-bold">Post</h1>
        </div>
      </div>

      {/* Post Content */}
      <div className="p-4">
        <div className="flex gap-3">
          <div className="w-12 h-12 rounded-full bg-gray-300 flex-shrink-0"></div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="font-bold text-gray-900">{post.author.username}</span>
              <span className="text-gray-500">@{post.author.username}</span>
            </div>
            <p className="text-sm text-gray-500 mt-1">{formatDate(post.created_at)}</p>
          </div>
        </div>

        {post.title && (
          <h2 className="text-2xl font-bold mt-4">{post.title}</h2>
        )}

        <div className="mt-4 text-lg whitespace-pre-wrap break-words">
          {post.content}
        </div>

        {/* Stats */}
        <div className="flex gap-4 mt-6 pt-4 border-t border-gray-200 text-sm text-gray-500">
          <span><strong className="text-gray-900">{likesCount}</strong> Likes</span>
          <span><strong className="text-gray-900">{post.comments_count || 0}</strong> Comments</span>
        </div>

        {/* Actions */}
        <div className="flex gap-8 mt-4 pt-4 border-t border-gray-200">
          <button
            onClick={handleLike}
            disabled={isLiking}
            className={`flex items-center gap-2 p-2 rounded-full transition-colors ${
              liked ? 'text-red-600' : 'text-gray-500 hover:text-red-600 hover:bg-red-50'
            }`}
          >
            <Heart className={`w-6 h-6 ${liked ? 'fill-current' : ''}`} />
          </button>
          <button className="flex items-center gap-2 p-2 rounded-full text-gray-500 hover:text-blue-600 hover:bg-blue-50 transition-colors">
            <MessageCircle className="w-6 h-6" />
          </button>
        </div>
      </div>

      {/* Comments */}
      <CommentSection
        postId={post.id.toString()}
        comments={post.comments || []}
        onCommentAdded={fetchPost}
      />
    </div>
  );
}
