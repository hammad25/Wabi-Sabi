from django import forms
from .models import Contact, Comment, UserProfile
from .widgets import CustomClearableFileInput

class UserProfileForm(forms.ModelForm):
    ''' Configure the profile form '''
    class Meta:
        ''' Form meta properties '''
        model = UserProfile
        fields = ('image', 'about',)

    # Replace the image field the the custom widget
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'about': 'Tell us who you are...',
        }

        for field in self.fields:
            if field != 'image':
                placeholder = f'{placeholders[field]}'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False

        # Add custom class to the image field
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'custom-image-input'


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': 3
    }))
    class Meta:
        model = Comment
        fields = ('body',) 


class ContactForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea(attrs={
        'style':'height:80px;'}))

    class Meta:
        model = Contact
        fields = '__all__'
