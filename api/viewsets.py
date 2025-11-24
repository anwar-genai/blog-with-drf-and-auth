from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from blog.models import Post, Comment, PollOption
from follows.models import Follow
from notifications.models import Notification
from .serializers import (
    PostSerializer, PostCreateSerializer, CommentSerializer,
    UserSerializer, FollowSerializer, NotificationSerializer,
    PollOptionSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('likes', 'comments', 'poll_options')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({'liked': liked, 'likes_count': post.likes.count()})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        post = self.get_object()
        if post.type != 'poll':
            return Response({'error': 'Not a poll'}, status=status.HTTP_400_BAD_REQUEST)
        
        option_ids = request.data.get('option_ids', [])
        if not option_ids:
            return Response({'error': 'No options selected'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(option_ids) > (post.max_choices or 1):
            return Response({'error': f'Maximum {post.max_choices} choices allowed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Remove existing votes (clear from all poll options for this post)
        for option in post.poll_options.all():
            option.voters.remove(request.user)
        
        # Add new votes
        for option_id in option_ids:
            try:
                option = PollOption.objects.get(id=option_id, post=post)
                option.voters.add(request.user)
            except PollOption.DoesNotExist:
                pass
        
        # Return updated poll options
        serializer = PollOptionSerializer(post.poll_options.all(), many=True, 
                                         context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get personalized feed for authenticated user"""
        if request.user.is_authenticated:
            following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
            posts = Post.objects.filter(author__in=following) | Post.objects.filter(author=request.user)
        else:
            posts = Post.objects.all()
        
        posts = posts.order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, username=None):
        user_to_follow = self.get_object()
        if user_to_follow == request.user:
            return Response({'error': 'Cannot follow yourself'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            following = False
        else:
            following = True
            # Create notification
            Notification.objects.create(
                user=user_to_follow,
                type='follow',
                message=f'{request.user.username} started following you',
                actor=request.user
            )
        
        return Response({'following': following})
    
    @action(detail=True, methods=['get'])
    def posts(self, request, username=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def followers(self, request, username=None):
        user = self.get_object()
        followers = Follow.objects.filter(following=user).select_related('follower')
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, username=None):
        user = self.get_object()
        following = Follow.objects.filter(follower=user).select_related('following')
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return Response({'status': 'All notifications marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})
