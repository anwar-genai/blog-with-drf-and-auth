const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface RequestOptions extends RequestInit {
  token?: string;
}

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return this.token;
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = `${API_URL}${endpoint}`;
    const token = options.token || this.getToken();

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      if (response.status === 401) {
        // Try to refresh token
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry the request with new token
          return this.request(endpoint, options);
        } else {
          this.clearToken();
          throw new Error('Authentication failed');
        }
      }
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    try {
      const response = await fetch(`${API_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        this.setToken(data.access);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
    return false;
  }

  // Auth endpoints
  async login(username: string, password: string) {
    const response = await this.request<{
      access: string;
      refresh: string;
    }>('/auth/token/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });

    this.setToken(response.access);
    localStorage.setItem('refresh_token', response.refresh);
    return response;
  }

  async register(username: string, email: string, password: string) {
    const response = await this.request<{
      user: any;
      access: string;
      refresh: string;
    }>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });

    this.setToken(response.access);
    localStorage.setItem('refresh_token', response.refresh);
    return response;
  }

  async getCurrentUser() {
    return this.request('/auth/me/');
  }

  async logout() {
    this.clearToken();
  }

  // Post endpoints
  async getPosts(page = 1) {
    return this.request(`/posts/?page=${page}`);
  }

  async getFeed(page = 1) {
    return this.request(`/posts/feed/?page=${page}`);
  }

  async getPost(id: string) {
    return this.request(`/posts/${id}/`);
  }

  async createPost(data: any) {
    return this.request('/posts/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async likePost(id: string) {
    return this.request(`/posts/${id}/like/`, {
      method: 'POST',
    });
  }

  async commentOnPost(id: string, content: string) {
    return this.request(`/posts/${id}/comment/`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }

  async voteOnPoll(postId: string, optionIds: number[]) {
    return this.request(`/posts/${postId}/vote/`, {
      method: 'POST',
      body: JSON.stringify({ option_ids: optionIds }),
    });
  }

  // User endpoints
  async getUser(username: string) {
    return this.request(`/users/${username}/`);
  }

  async getUserPosts(username: string, page = 1) {
    return this.request(`/users/${username}/posts/?page=${page}`);
  }

  async followUser(username: string) {
    return this.request(`/users/${username}/follow/`, {
      method: 'POST',
    });
  }

  async getFollowers(username: string) {
    return this.request(`/users/${username}/followers/`);
  }

  async getFollowing(username: string) {
    return this.request(`/users/${username}/following/`);
  }

  // Notification endpoints
  async getNotifications() {
    return this.request('/notifications/');
  }

  async markNotificationRead(id: string) {
    return this.request(`/notifications/${id}/mark_read/`, {
      method: 'POST',
    });
  }

  async markAllNotificationsRead() {
    return this.request('/notifications/mark_all_read/', {
      method: 'POST',
    });
  }
}

export const api = new ApiClient();
export default api;
