from django.shortcuts import render
from . forms import ContactForm
from .models import Post

# Create your views here.

def home(request):
    return render(request, 'blog/index.html')



def about_view(request):
    return render(request, 'blog/about.html')


def contact_view(request):
    form = ContactForm()
    context = {
        'form' : form
    }
    return render(request, 'blog/contact.html', context)