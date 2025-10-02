from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Post(models.Model):
    class PostType(models.TextChoices):
        ARTICLE = 'article', 'Article'
        POST = 'post', 'Post'
        POLL = 'poll', 'Poll'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    type = models.CharField(max_length=20, choices=PostType.choices, default=PostType.ARTICLE)
    # Poll controls
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    max_choices = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def is_poll(self) -> bool:
        return self.type == Post.PostType.POLL

    @property
    def poll_is_open(self) -> bool:
        if not self.is_poll:
            return False
        now = timezone.now()
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        return True

    def _generate_unique_slug(self) -> str:
        base_slug = slugify(self.title) or 'post'
        slug_candidate = base_slug
        suffix = 2
        while Post.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
            slug_candidate = f"{base_slug}-{suffix}"
            suffix += 1
        return slug_candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


class PollOption(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='poll_options')
    text = models.CharField(max_length=255)
    voters = models.ManyToManyField(User, related_name='voted_poll_options', blank=True)

    def __str__(self) -> str:
        return f"Option({self.text}) for {self.post.title}"

    @property
    def votes_count(self) -> int:
        return self.voters.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post}"

# Create your models here.
