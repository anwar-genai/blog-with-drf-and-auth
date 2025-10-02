from django.contrib import admin
from .models import Post, Comment, PollOption


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'created_at', 'updated_at', 'likes_count')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at', 'type')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__username')


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('post', 'text', 'votes_count')

# Register your models here.
