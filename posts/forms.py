from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_thumbnail']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
        }
