from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ContactForm, CommentForm, UserProfileForm
from .models import Post, Comment, UserProfile


# Create your views here.

class PostList(generic.ListView):
    """
    A class that renders the blog post on the template
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 6
    template_name = 'blog/articles.html'


class PostDetail(View):
    """
    Fetches post content from a unique slug.
    Also returns a list of comments by users
    """

    def get(self, request, slug, *args, **kwargs):
        """
        Fucntion for displaying the contents of the blog post
        """
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        is_favourite = False
        if post.favourite.filter(id=self.request.user.id).exists():
            is_favourite = True

        return render(
            request,
            'blog/post_detail.html',
            {
                'post': post,
                'comments': comments,
                'liked': liked,
                'is_favourite': is_favourite,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Function for making chnages to the interactivity of the blog
        """
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        is_favourite = False
        if post.favourite.filter(id=self.request.user.id).exists():
            is_favourite = True

        # adds users comments to the post
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
                'post': post,
                'comments': comments,
                'liked': liked,
                'is_favourite': is_favourite,
                'comment_form': comment_form,
            },
        )


def update_comment(request, pk):
    """
    Function for updating a comment
    """
    slug = request.POST['slug']
    comment_id = request.POST['edit_comment_id']
    comment_body = request.POST[str(comment_id) + '_comment_edit_content']
    comment = get_object_or_404(Comment, pk=pk)
    comment.body = comment_body
    comment.save(force_update=True)
    return redirect('post_detail', slug=slug)


def delete_comment(request, pk):
    """
    Funtion for deleting a comment
    """
    if request.method == "POST":
        slug = request.POST['postSlug']
        comment = get_object_or_404(Comment, pk=pk)
        try:
            comment.delete()
        except:
            print("server error")
    return redirect('post_detail', slug=slug)


class PostLike(View):
    """
    Handling the like functionality
    """
    def post(self, request, slug):
        """
        Add and removes like to the post
        """
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def favourite_post(request, slug):
    """
    Fuction to bookmark and unbookmark a post by the user
    """
    post = get_object_or_404(Post, slug=slug)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)

    return redirect('post_detail', slug=slug)


def favourite_post_list(request):
    """
    Function to display the favourite post
    """
    user = request.user
    fav_post = user.favourite.all()
    context = {
        'fav_post': fav_post
    }
    return render(request, 'blog/favourite.html', context)


# def favorites_blog(request, slug):
#     user_favposts = get_object_or_404(Post, slug=slug)
#     query = FavoritePost.objects.filter(post=user_favposts,
#                    user=request.user)
#     if not query:
#         favpost = FavoritePost(post=user_favposts, user=request.user)
#         favpost.save()
#     else:
#         favpost.delete()

#     return HttpResponseRedirect(reverse('post_detail', args=[slug]))

@login_required
def profile(request):
    '''Display and Edit user profile info'''
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user = User.objects.get(username=request.user.username)

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

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'something went wrong')

    profile_form = UserProfileForm(instance=user_profile)
    context = {
        'profile_form': profile_form,
        'user_profile': user_profile,
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
    """
    Function to display the sign up page
    """
    return render(register, 'account/signup.html')


def home(request):
    """
    Function to display the home page
    """
    return render(request, 'blog/index.html')


def about_view(request):
    """
    Function to display the about page
    """
    return render(request, 'blog/about.html')


def contact_add(request):
    """
    Function to display the success page for contact
    """
    return render(request, 'blog/success.html')


def contact_view(request):
    """
    Function to send a contact form to the admin
    """
    if request.method == "GET":
        contact_form = ContactForm()
        context = {'contact_form': contact_form}
        return render(request, 'blog/contact.html', context)
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
        return redirect('contactadd')
