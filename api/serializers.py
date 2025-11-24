from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Comment, PollOption
from accounts.models import Profile
from follows.models import Follow
from notifications.models import Notification


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'date_joined', 'profile', 'followers_count', 'following_count']
    
    def get_profile(self, obj):
        try:
            return ProfileSerializer(obj.profile).data
        except Profile.DoesNotExist:
            return None
    
    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()
    
    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class PollOptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    user_voted = serializers.SerializerMethodField()
    
    class Meta:
        model = PollOption
        fields = ['id', 'text', 'votes_count', 'percentage', 'user_voted']
    
    def get_votes_count(self, obj):
        return obj.voters.count()
    
    def get_percentage(self, obj):
        total_votes = sum(opt.voters.count() for opt in obj.post.poll_options.all())
        if total_votes == 0:
            return 0
        return round((obj.voters.count() / total_votes) * 100, 1)
    
    def get_user_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.voters.filter(id=request.user.id).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    poll_options = PollOptionSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'slug', 'title', 'content', 'type', 'author', 
                  'created_at', 'updated_at', 'starts_at', 'ends_at', 
                  'max_choices', 'comments', 'poll_options', 
                  'likes_count', 'comments_count', 'user_liked']
        read_only_fields = ['slug', 'author', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    poll_options = serializers.ListField(
        child=serializers.CharField(max_length=200),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'type', 'starts_at', 'ends_at', 
                  'max_choices', 'poll_options']
    
    def create(self, validated_data):
        poll_options_data = validated_data.pop('poll_options', [])
        post = Post.objects.create(**validated_data)
        
        if post.type == 'poll' and poll_options_data:
            for option_text in poll_options_data:
                PollOption.objects.create(post=post, text=option_text)
        
        return post


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['created_at']


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'type', 'message', 'actor', 'url', 
                  'read', 'created_at']
        read_only_fields = ['created_at']
