from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Follow


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'follows/index.html')


@login_required
def people(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q', '').strip()
    users = User.objects.exclude(pk=request.user.pk)
    if q:
        users = users.filter(username__icontains=q)
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    return render(request, 'follows/people.html', { 'users': users, 'following_ids': following_ids, 'q': q })


@login_required
def toggle_follow(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('follows:people')
    rel, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        rel.delete()
        messages.info(request, f'Unfollowed {target.username}.')
    else:
        messages.success(request, f'Now following {target.username}.')
    return redirect('follows:people')
