from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from . forms import ContactForm, CommentForm
from .models import Post, Comment, Contact


# Create your views here.

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/articles.html'


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
    
        return render(
            request,
            'blog/post_detail.html',
            {
                'post':post,
                'comments':comments,
                'liked':liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
    
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.username = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'blog/post_detail.html',
            {
                'post':post,
                'comments':comments,
                'liked':liked,
                'comment_form': CommentForm()
            },
        )



def signup(register):
    return render(request, 'account/signup.html')

def home(request):
    return render(request, 'blog/index.html')

def about_view(request):
    return render(request, 'blog/about.html')

def contact_add(request):
    return render(request, 'blog/success.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'blog/success.html')
    form = ContactForm()
    context = {
        'form' : form
    }
    return render(request, 'blog/contact.html', context)