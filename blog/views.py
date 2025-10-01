from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm, CommentForm


def index(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.select_related('author').prefetch_related('likes').all()
    paginator = Paginator(qs, 15)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', { 'posts': posts })


def home(request: HttpRequest) -> HttpResponse:
    latest_posts = Post.objects.select_related('author').prefetch_related('likes').all()[:5]
    return render(request, 'home.html', { 'posts': latest_posts })


def detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('likes', 'comments__author'), slug=slug)
    comment_form = CommentForm()
    return render(request, 'blog/detail.html', { 'post': post, 'comment_form': comment_form })


@login_required
def create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', { 'form': form, 'title': 'Create Post' })


@login_required
def edit(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', { 'form': form, 'title': 'Edit Post' })


@login_required
def delete(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('blog:index')
    return render(request, 'blog/confirm_delete.html', { 'post': post })


@login_required
def toggle_like(request: HttpRequest, slug: str) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.info(request, 'Unliked post')
    else:
        post.likes.add(request.user)
        messages.success(request, 'Liked post')
    return redirect('blog:detail', slug=slug)


@login_required
def add_comment(request: HttpRequest, slug: str) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Comment added!')
    return redirect('blog:detail', slug=slug)
