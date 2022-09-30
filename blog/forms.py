from django import forms
from . models import Contact, Comment

class CommentForm(forms.ModelForm):

    body = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': 3
    }))
    class Meta:
        model = Comment
        fields = ('body',) 


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
