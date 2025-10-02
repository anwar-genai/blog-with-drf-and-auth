from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Notification
from django.http import HttpRequest, HttpResponseNotAllowed


@login_required
def read_all(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def list_notifications(request: HttpRequest):
    items = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    return render(request, 'notifications/list.html', { 'items': items })


