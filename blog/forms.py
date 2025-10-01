from django import forms
from .widgets import CustomCKEditorWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control post-title-input',
                'placeholder': 'Post title',
                'autocomplete': 'off',
            }),
            'content': CustomCKEditorWidget(config_name='default'),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

