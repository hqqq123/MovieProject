from django.contrib import admin

# Register your models here.
from blog.models import Tag, Post, Category

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)