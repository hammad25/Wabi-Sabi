from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from .forms import ContactForm, CommentForm, UserProfileForm
from .models import Post, Comment, Contact, UserProfile
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/articles.html'


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('-created_on')
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
            comment = comment_form.save(commit=False)
            comment.email = request.user.email
            comment.name = request.user
            comment.username = request.user.username
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)

        return render(
            request,
            'blog/post_detail.html',
            {
                'post':post,
                'comments':comments,
                'liked':liked,
                'comment_form': comment_form,
            },
        )

def delete_comment_confirm(request):
    return render(request, 'blog/delete_comment_confirm.html')

def delete_comment(request, id, pk):
    comment = get_object_or_404(Comment,  )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def profile(request):
    '''Display and Edit user profile info'''
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user = User.objects.get(username= request.user.username)


    if request.method == 'POST':
        # update user profile info
        profile_form = UserProfileForm(request.POST, request.FILES,
                                         instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()

            # Update User info
            user = User.objects.get(username=request.user.username)
            username = request.POST['username']
            email = request.POST['email']
            user.username = username
            user.email = email
            user.save()


    profile_form = UserProfileForm(instance=user_profile)
    context = {
        'profile_form':profile_form,
        'user_profile':user_profile,
    }

    return render(request, 'blog/profile.html', context)

@login_required
def delete_profile(request):
    ''' Delete the user profile and the user '''

    user = User.objects.get(username=request.user.username)

    if request.method == 'POST':
        user.delete()

        messages.success(request, 'Your profile was deleted successfuly')
        return redirect('home')

def signup(register):
    return render(request, 'account/signup.html')

def home(request):
    return render(request, 'blog/index.html')

def about_view(request):
    return render(request, 'blog/about.html')

def contact_add(request):
    return render(request, 'blog/success.html')


def contact_view(request):
    if request.method == "GET":
        contact_form = ContactForm()
        context = {'contact_form' : contact_form}
        return render(request, 'blog/contact.html', context)
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
        return redirect('contactadd')
