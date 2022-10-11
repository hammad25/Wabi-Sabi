from django.contrib import admin
from .models import Post, Comment, Contact, Category, UserProfile, FavoritePost
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on', 'category')
    search_fields = ['title', 'category']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on', 'category', )
    summernote_fields = ('content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','name', 'body', 'created_on')
    list_filter = ('created_on', 'post')
    search_fields = ['name', 'body']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('created_on',)

admin.site.register(Category)

admin.site.register(UserProfile)