from tinymce.widgets import TinyMCE
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# Apply summernote to specific fields.


class SomeForm(forms.Form):
    foo = forms.CharField(widget=SummernoteWidget())


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(
        attrs={'cols': 80, 'rows': 50, 'class': 'form-control'}))
