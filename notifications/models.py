from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    # Optional actor (e.g., follower) and target URL to visit
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_sent')
    url = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


