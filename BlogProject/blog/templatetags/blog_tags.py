from django import template
from django.db.models import Count

from blog.models import Category, Tag, Post

register = template.Library()

@register.simple_tag
def get_categories():
    """获取博客的所有分类"""
    return Category.objects.annotate(post_num=Count('post')).filter(post_num__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(post_num=Count('post')).filter(post_num__gt=0)

@register.simple_tag
def get_recent_posts(num=3):
    return Post.objects.order_by('-created_time').all()[:num]

@register.simple_tag
def get_archive():
    return Post.objects.dates('created_time','month','DESC')