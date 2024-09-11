from django import forms
from markdownx.fields import MarkdownxFormField

from zanhu.articles.models import Article


class ArticleForms(forms.ModelForm):

    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    content = MarkdownxFormField()
    class Meta:
        model = Article
        fields = ["title", "content", "tags", "image", "status", "edited"]
