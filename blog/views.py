from django.shortcuts import render
from . forms import ContactForm

# Create your views here.






def contact_view(request):
    form = ContactForm()
    context = {
        'form' : form
    }
    return render(request, 'blog/contact.html', context)