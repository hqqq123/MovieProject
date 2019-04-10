from django.urls import path

from blog.views import index, detail, category, tag, archive

urlpatterns = [
    path('',index,name='index'),
    path('detail/<int:id>/', detail, name='detail'),
    path('category/<int:id>/', category, name='category'),
    path('tag/<int:id>/', tag, name='tag'),
    path('archive/<int:year>/<int:month>/', archive, name='archive'),

]