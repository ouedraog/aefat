from django import forms

from aefat.articles.models import Article
from ckeditor.fields import RichTextFormField


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255)
    content = RichTextFormField()
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')

    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'status']
