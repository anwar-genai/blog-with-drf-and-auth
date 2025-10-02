from django import forms
from .widgets import CustomCKEditorWidget
from .models import Post, Comment, PollOption


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'type', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control post-title-input',
                'placeholder': 'Post title',
                'autocomplete': 'off',
            }),
            'content': CustomCKEditorWidget(config_name='default'),
        }


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['text']


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control post-title-input',
                'placeholder': 'Article title',
                'autocomplete': 'off',
            }),
            'content': CustomCKEditorWidget(config_name='default'),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = Post.PostType.ARTICLE
        if commit:
            instance.save()
        return instance


class StatusPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': "What's on your mind?",
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Content is required.')
        return content

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = Post.PostType.POST
        instance.title = instance.title or ''
        if commit:
            instance.save()
        return instance


class PollPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'starts_at', 'ends_at', 'max_choices']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control post-title-input',
                'placeholder': 'Poll question',
                'autocomplete': 'off',
            }),
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'ends_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = Post.PostType.POLL
        instance.content = ''
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

