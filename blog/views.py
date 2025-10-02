from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
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
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('likes', 'comments__author', 'poll_options__voters'), slug=slug)
    comment_form = CommentForm()
    # Build poll context
    options_data = []
    total_votes = 0
    if getattr(post, 'is_poll', False):
        for opt in post.poll_options.all():
            total_votes += opt.votes_count
        user_voted_option_ids = set()
        if request.user.is_authenticated:
            for opt in post.poll_options.all():
                if opt.voters.filter(pk=request.user.pk).exists():
                    user_voted_option_ids.add(opt.pk)
        for opt in post.poll_options.all():
            percent = 0
            if total_votes > 0:
                percent = int(round((opt.votes_count / total_votes) * 100))
            options_data.append({
                'id': opt.pk,
                'text': opt.text,
                'votes': opt.votes_count,
                'percent': percent,
                'selected': opt.pk in user_voted_option_ids,
            })
        return render(request, 'blog/detail.html', {
            'post': post,
            'comment_form': comment_form,
            'poll_total_votes': total_votes,
            'poll_options': options_data,
        })
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
    post = get_object_or_404(Post.objects.prefetch_related('poll_options__voters'), slug=slug)
    if not getattr(post, 'is_poll', False) or not post.poll_is_open:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': 'Poll is closed.'}, status=400)
        return redirect('blog:detail', slug=slug)
    option = get_object_or_404(PollOption, pk=option_id, post=post)

    # Determine current selections by user
    user = request.user
    if not user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': 'Login required.'}, status=403)
        messages.error(request, 'Login required to vote.')
        return redirect('accounts:login')

    # Toggle logic respecting max_choices
    already_selected = option.voters.filter(pk=user.pk).exists()
    if already_selected:
        option.voters.remove(user)
    else:
        if post.max_choices <= 1:
            # Clear previous and add this one
            for opt in post.poll_options.all():
                opt.voters.remove(user)
            option.voters.add(user)
        else:
            current_count = 0
            for opt in post.poll_options.all():
                if opt.voters.filter(pk=user.pk).exists():
                    current_count += 1
            if current_count >= post.max_choices:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'ok': False, 'error': f'Max {post.max_choices} selections allowed.'}, status=400)
                messages.error(request, f'Max {post.max_choices} selections allowed.')
                return redirect('blog:detail', slug=slug)
            option.voters.add(user)

    # Build JSON response if AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_votes = 0
        options = []
        user_selected_ids = set()
        for opt in post.poll_options.all():
            total_votes += opt.votes_count
        for opt in post.poll_options.all():
            if opt.voters.filter(pk=user.pk).exists():
                user_selected_ids.add(opt.pk)
        for opt in post.poll_options.all():
            percent = 0
            if total_votes > 0:
                percent = int(round((opt.votes_count / total_votes) * 100))
            options.append({
                'id': opt.pk,
                'text': opt.text,
                'votes': opt.votes_count,
                'percent': percent,
                'selected': opt.pk in user_selected_ids,
            })
        return JsonResponse({'ok': True, 'total': total_votes, 'options': options, 'max': post.max_choices})

    messages.success(request, 'Vote updated!')
    return redirect('blog:detail', slug=slug)
