from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, PollOption
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import (
    PostForm,
    CommentForm,
    ArticlePostForm,
    StatusPostForm,
    PollPostForm,
)


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
    return render(request, 'blog/type_select.html')


@login_required
def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Article created!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = ArticlePostForm()
    return render(request, 'blog/form.html', { 'form': form, 'title': 'Create Article', 'show_poll_fields': False })


@login_required
def create_status(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = StatusPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = StatusPostForm()
    return render(request, 'blog/form.html', { 'form': form, 'title': 'Create Post', 'show_poll_fields': False })


@login_required
def create_poll(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PollPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            option_texts = [
                request.POST.get('option1', '').strip(),
                request.POST.get('option2', '').strip(),
                request.POST.get('option3', '').strip(),
                request.POST.get('option4', '').strip(),
            ]
            for text in option_texts:
                if text:
                    PollOption.objects.create(post=post, text=text)
            messages.success(request, 'Poll created!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PollPostForm()
    return render(request, 'blog/form.html', { 'form': form, 'title': 'Create Poll', 'show_poll_fields': True })


@login_required
def edit(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            if getattr(post, 'is_poll', False):
                post.poll_options.all().delete()
                option_texts = [
                    request.POST.get('option1', '').strip(),
                    request.POST.get('option2', '').strip(),
                    request.POST.get('option3', '').strip(),
                    request.POST.get('option4', '').strip(),
                ]
                for text in option_texts:
                    if text:
                        PollOption.objects.create(post=post, text=text)
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


@login_required
def vote_poll(request: HttpRequest, slug: str, option_id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    post = get_object_or_404(Post, slug=slug)
    if not getattr(post, 'is_poll', False):
        return redirect('blog:detail', slug=slug)
    option = get_object_or_404(PollOption, pk=option_id, post=post)
    # Remove any previous votes by this user for this poll
    for opt in post.poll_options.all():
        opt.voters.remove(request.user)
    option.voters.add(request.user)
    messages.success(request, 'Vote recorded!')
    return redirect('blog:detail', slug=slug)
