from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from blog.models import Post


def index(request):
    posts=Post.objects.all()
    PageObj=Paginator(posts,per_page=1)
    page=request.GET.get('page',1)
    print(page)
    try:
        postsPageObj=PageObj.page(page)
        posts=postsPageObj.object_list
    except(EmptyPage,PageNotAnInteger):
        posts=PageObj.page(1).object_list


    return render(request, 'blog/index.html', context={
        'posts': posts,
        'postsPageObj': postsPageObj
    })

def detail(request,id):
    post=Post.objects.filter(id=id).first()


    return render(request,'blog/detaile.html',context={
        'post':post
    })

def get_pageObj(request,posts):
    PageObj = Paginator(posts, per_page=1)
    page = request.GET.get('page', 1)

    postsPageObj = PageObj.page(page)
    return postsPageObj
def category(request,id):
    posts=Post.objects.filter(category_id=id).all()
    postsPageObj=get_pageObj(request,posts)
    posts=postsPageObj.object_list

    return render(request,'blog/index.html',context={
        'posts':posts,
        'postsPageObj': postsPageObj
    })
def tag(request,id):
    posts=Post.objects.filter(tags=id).all()
    postsPageObj=get_pageObj(request,posts)
    posts=postsPageObj.object_list

    return render(request,'blog/index.html',context={
        'posts':posts,
        'postsPageObj': postsPageObj
    })

def archive(request,year,month):

    posts=Post.objects.filter(created_time__year=year).all()
    postsPageObj=get_pageObj(request,posts)
    posts=postsPageObj.object_list
    return render(request,'blog/index.html',context={
        'posts':posts,
        'postsPageObj': postsPageObj
    })