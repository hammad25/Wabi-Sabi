from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS = ((0, "Draft"), (1, "Published"))
QUERY_TYPE = ((0, "Question"), (1, "Contribute"))


class Category(models.Model):
    """
    A class to group posts according to category
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ('home')


class Post(models.Model):
    """
    A class for the Blog Application that stores
    variable names with field types for blog posts.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)
    favourite = models.ManyToManyField(
        User, related_name='favourite', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """
    A class that handles the comments section within each post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name="comments")
    name = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Contact(models.Model):
    """
    A class that handles the contact information
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    query_type = models.IntegerField(choices=QUERY_TYPE, default=0)
    email = models.EmailField()
    message = models.TextField(default="Type your message her")
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} contacted you."


# Profile
class FavoritePost(models.Model):
    ''' Model that define the favorites post database design '''

    class Meta:
        '''Set verbose name'''
        verbose_name_plural = 'Favorites Blogs'

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                    related_name='favorites_blog')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL,
                            null=True, blank=True,)


class UserProfile(models.Model):
    ''' Model that define user profile information '''
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_profile')
    about = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    make_public = models.BooleanField(default=False)

    def __str__(self):
        ''' Return the username '''
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    ''' Create or upadte the user profile '''
    if created:
        UserProfile.objects.create(user=instance)
    # If existing user, just save
    instance.user_profile.save()
