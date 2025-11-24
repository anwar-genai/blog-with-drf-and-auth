'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Image, Film, BarChart3, Smile, Calendar, MapPin } from 'lucide-react';
import api from '@/lib/api';

interface ComposePostProps {
  onPostCreated?: () => void;
}

export default function ComposePost({ onPostCreated }: ComposePostProps) {
  const { isAuthenticated, user } = useAuth();
  const [content, setContent] = useState('');
  const [isPosting, setIsPosting] = useState(false);
  
  if (!isAuthenticated) {
    return null; // Don't show compose form if not logged in
  }

  const handleSubmit = async () => {
    if (!content.trim() || isPosting) return;

    setIsPosting(true);
    try {
      await api.createPost({
        title: content.trim().substring(0, 50), // Use first 50 chars as title
        content: content.trim(),
        type: 'post',
      });
      setContent('');
      if (onPostCreated) onPostCreated();
    } catch (error) {
      console.error('Failed to create post:', error);
      alert('Failed to create post. Please try again.');
    } finally {
      setIsPosting(false);
    }
  };

  return (
    <div className="border-b border-gray-200 p-4">
      <div className="flex gap-3">
        <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold flex-shrink-0">
          {user?.username?.[0]?.toUpperCase() || 'U'}
        </div>
        
        <div className="flex-1">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="What's happening?"
            className="w-full resize-none border-none outline-none text-xl placeholder-gray-500 min-h-[60px]"
            rows={2}
          />
          
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center gap-4">
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <Image className="w-5 h-5" />
              </button>
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <Film className="w-5 h-5" />
              </button>
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <BarChart3 className="w-5 h-5" />
              </button>
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <Smile className="w-5 h-5" />
              </button>
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <Calendar className="w-5 h-5" />
              </button>
              <button className="text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-colors">
                <MapPin className="w-5 h-5" />
              </button>
            </div>
            
            <button
              onClick={handleSubmit}
              disabled={!content.trim() || isPosting}
              className={`
                px-4 py-1.5 rounded-full font-semibold transition-colors
                ${content.trim() && !isPosting
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-blue-200 text-white cursor-not-allowed'
                }
              `}
            >
              {isPosting ? 'Posting...' : 'Post'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
