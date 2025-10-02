from django.contrib.auth.models import AnonymousUser
from notifications.models import Notification
from follows.models import Follow


def unread_notifications(request):
    user = getattr(request, 'user', None)
    if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
        return { 'unread_notifications_count': 0, 'recent_notifications': [], 'following_ids': set() }
    count = Notification.objects.filter(user=user, read=False).count()
    recent = list(Notification.objects.filter(user=user).select_related('actor').order_by('-created_at')[:5])
    following_ids = set(Follow.objects.filter(follower=user).values_list('following_id', flat=True))
    return { 'unread_notifications_count': count, 'recent_notifications': recent, 'following_ids': following_ids }


