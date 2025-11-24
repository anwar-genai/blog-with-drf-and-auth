'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { Heart, MessageCircle, Share, MoreHorizontal } from 'lucide-react';
import api from '@/lib/api';

interface Post {
  id: number;
  slug: string;
  title?: string;
  content: string;
  type: string;
  author: {
    id: number;
    username: string;
    profile?: {
      avatar?: string;
    };
  };
  created_at: string;
  likes_count: number;
  comments_count: number;
  user_liked: boolean;
  poll_options?: any[];
}

interface PostCardProps {
  post: Post;
  onUpdate?: () => void;
}

export default function PostCard({ post, onUpdate }: PostCardProps) {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [liked, setLiked] = useState(post.user_liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isLiking, setIsLiking] = useState(false);

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
      if (error instanceof Error && error.message.includes('Authentication')) {
        router.push('/login');
      }
    } finally {
      setIsLiking(false);
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

    if (days > 0) return `${days}d`;
    if (hours > 0) return `${hours}h`;
    if (minutes > 0) return `${minutes}m`;
    return 'now';
  };

  return (
    <article className="border-b border-gray-200 hover:bg-gray-50 transition-colors duration-200">
      <div className="p-4">
        <div className="flex gap-3">
          {/* Avatar */}
          <Link href={`/profile/${post.author.username}`}>
            <div className="w-12 h-12 rounded-full bg-gray-300 flex-shrink-0 overflow-hidden">
              {post.author.profile?.avatar ? (
                <img 
                  src={post.author.profile.avatar} 
                  alt={post.author.username}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-600 font-semibold">
                  {post.author.username[0].toUpperCase()}
                </div>
              )}
            </div>
          </Link>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1 text-sm">
              <Link 
                href={`/profile/${post.author.username}`}
                className="font-bold text-gray-900 hover:underline"
              >
                {post.author.username}
              </Link>
              <span className="text-gray-500">@{post.author.username}</span>
              <span className="text-gray-500">·</span>
              <span className="text-gray-500">{formatDate(post.created_at)}</span>
              {post.type !== 'post' && (
                <span className={`ml-2 px-2 py-0.5 text-xs rounded-full ${
                  post.type === 'article' ? 'bg-blue-100 text-blue-800' :
                  post.type === 'poll' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {post.type}
                </span>
              )}
            </div>

            {post.title && (
              <h3 className="font-semibold text-lg mt-1">{post.title}</h3>
            )}

            <Link href={`/post/${post.slug}`}>
              <div className="mt-2 text-gray-900 whitespace-pre-wrap break-words">
                {post.content}
              </div>
            </Link>

            {/* Poll Options */}
            {post.type === 'poll' && post.poll_options && (
              <div className="mt-3 space-y-2">
                {post.poll_options.map((option: any) => (
                  <div 
                    key={option.id}
                    className="border border-gray-300 rounded-full p-3 hover:bg-gray-50 cursor-pointer"
                  >
                    <div className="flex justify-between items-center">
                      <span>{option.text}</span>
                      <span className="text-sm text-gray-500">
                        {option.percentage}%
                      </span>
                    </div>
                    {option.votes_count > 0 && (
                      <div className="mt-1 bg-gray-200 rounded-full h-1">
                        <div 
                          className="bg-blue-500 h-1 rounded-full transition-all duration-300"
                          style={{ width: `${option.percentage}%` }}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-between mt-3 -ml-2">
              <Link href={`/post/${post.slug}`} className="flex items-center gap-1 p-2 rounded-full hover:bg-blue-50 hover:text-blue-600 transition-colors group">
                <MessageCircle className="w-5 h-5" />
                <span className="text-sm text-gray-500 group-hover:text-blue-600">
                  {post.comments_count}
                </span>
              </Link>

              <button className="flex items-center gap-1 p-2 rounded-full hover:bg-green-50 hover:text-green-600 transition-colors">
                <Share className="w-5 h-5" />
              </button>

              <button 
                onClick={handleLike}
                disabled={isLiking}
                className={`flex items-center gap-1 p-2 rounded-full transition-colors group ${
                  liked 
                    ? 'text-red-600 hover:bg-red-50' 
                    : 'hover:bg-red-50 hover:text-red-600'
                }`}
              >
                <Heart 
                  className={`w-5 h-5 ${liked ? 'fill-current' : ''}`}
                />
                <span className={`text-sm ${
                  liked ? 'text-red-600' : 'text-gray-500 group-hover:text-red-600'
                }`}>
                  {likesCount}
                </span>
              </button>

              <button className="p-2 rounded-full hover:bg-gray-100 transition-colors">
                <MoreHorizontal className="w-5 h-5 text-gray-500" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}
