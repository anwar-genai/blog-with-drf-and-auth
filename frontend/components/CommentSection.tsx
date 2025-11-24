'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface Comment {
  id: number;
  author: {
    username: string;
    profile?: {
      avatar?: string;
    };
  };
  content: string;
  created_at: string;
}

interface CommentSectionProps {
  postId: string;
  comments: Comment[];
  onCommentAdded?: () => void;
}

export default function CommentSection({ postId, comments, onCommentAdded }: CommentSectionProps) {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [localComments, setLocalComments] = useState(comments);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (!content.trim() || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const newComment = await api.commentOnPost(postId, content.trim());
      setLocalComments([...localComments, newComment]);
      setContent('');
      if (onCommentAdded) onCommentAdded();
    } catch (error) {
      console.error('Failed to post comment:', error);
      if (error instanceof Error && error.message.includes('Authentication')) {
        router.push('/login');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'just now';
  };

  return (
    <div className="border-t border-gray-200 mt-4">
      {/* Comment Form */}
      {isAuthenticated ? (
        <form onSubmit={handleSubmit} className="p-4 border-b border-gray-200">
          <div className="flex gap-3">
            <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold flex-shrink-0">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1">
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Post your reply..."
                className="w-full border border-gray-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                rows={3}
              />
              <div className="flex justify-end mt-2">
                <button
                  type="submit"
                  disabled={!content.trim() || isSubmitting}
                  className="px-4 py-2 bg-blue-500 text-white rounded-full font-semibold hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isSubmitting ? 'Posting...' : 'Reply'}
                </button>
              </div>
            </div>
          </div>
        </form>
      ) : (
        <div className="p-4 text-center bg-gray-50">
          <p className="text-gray-600">
            <button
              onClick={() => router.push('/login')}
              className="text-blue-500 hover:underline font-medium"
            >
              Sign in
            </button>
            {' '}to comment
          </p>
        </div>
      )}

      {/* Comments List */}
      <div>
        {localComments.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            No comments yet. Be the first to comment!
          </div>
        ) : (
          localComments.map((comment) => (
            <div key={comment.id} className="p-4 border-b border-gray-200 hover:bg-gray-50 transition-colors">
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-gray-300 flex-shrink-0"></div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-bold">{comment.author.username}</span>
                    <span className="text-gray-500 text-sm">@{comment.author.username}</span>
                    <span className="text-gray-500 text-sm">· {formatDate(comment.created_at)}</span>
                  </div>
                  <p className="mt-1 text-gray-900 whitespace-pre-wrap">{comment.content}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
